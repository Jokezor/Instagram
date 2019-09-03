'''
	Used to iniate the database
'''

import mysql.connector
import os

# Returns the path for the files
def Get_path_info():

	# File with your login to database such as host, user = 'your_user' and pass = 'your_password' (Need single quotes)
	path_db = '/Users/Newera/Documents/Instagram_non_git/database_info/database_info.txt'

	# Contains the name of your account which will be used to create db.
	path_acc = '/Users/Newera/Documents/Instagram_non_git/account_info/account_info.txt'

	# Text file which includes the pages for each theme.
	path_pages = '/Users/Newera/Documents/Instagram_non_git/account_info/pages.txt'

	# Create list
	paths = [path_db, path_acc, path_pages]

	return paths


# Read database information from file
def read_database_data(path):
	# open file
	db_file = open(path,'r')
	
	# Read authentication data
	auth = db_file.readlines()

	host = auth[0].split('\'')[1]
	user = auth[1].split('\'')[1]
	password = auth[2].split('\'')[1]

	# close file
	db_file.close()

	return host, user, password

# Read account information from file
def read_account_data(path):

	# open file
	acc_file = open(path,'r')

	# Read accounts
	accounts = acc_file.readlines()

	# Acc info of the theme: {account: theme}
	Acc_info = {}

	# Remove extra stuff
	for i in range(0, len(accounts)):
		acc = accounts[i].split('\'')[1].split(',')[0]

		# Remove trailing newline
		if '\n' in acc:
			acc = acc.split('\n')[0]

		# Add empty list
		if acc not in Acc_info:
			Acc_info[acc] = []

		# Theme
		themes = accounts[i].split('#')[1].split(',')

		for theme in themes:
			# Remove newline
			if '\n' in theme:
				theme = theme.split('\n')[0]

			# Add the data
			Acc_info[acc].append(theme)


		



	# close file
	acc_file.close()

	return Acc_info

# Read pages information from file
def read_pages_data(path):

	# open file
	pages_file = open(path,'r')
	# Read accounts
	pages = pages_file.readlines()

	# Remove extra stuff
	# Theme
	# Store: {'theme': {pages}}
	Pages_dict = {}

	for i in range(0, len(pages)):

		# Remove comments and empty lines
		if not pages[i].startswith('%') and not pages[i].startswith('\n'):

			# Get themes by hashtags
			if pages[i].startswith('#'):
				themes = pages[i].split('#')[1].split(',')
			
			# Acceses pages if not currently at theme line
			if not pages[i].startswith('#'):
				
				for theme in themes:
					
					# If the newline is coded then remove it
					if '\n' in theme:
						theme = theme.split('\n')[0]
					
					# First need to build list
					if not theme in Pages_dict:
						Pages_dict[theme] = []

					# If the newline is coded then remove it
					if '\n' in pages[i]:
						Pages_dict[theme].append(pages[i].split('\n')[0])
					else:
						Pages_dict[theme].append(pages[i])

	# close file
	pages_file.close()

	return Pages_dict

# Checks if the database is already existing
def exists_database(accounts, mydb):

	mycursor = mydb.cursor()

	mycursor.execute("SHOW DATABASES")

	# Need to get databases, is removed when read from mycursor
	dbs = [db for db in mycursor]
	
	# List of the accounts to add databases for
	accounts_to_add = []

	for acc_name in accounts:
		
		if not any(acc_name in db for db in dbs):
			accounts_to_add.append(acc_name)
	
	return accounts_to_add

# Connect to "ground" database and return cursor
def connect_db(host, user, password):
	mydb = mysql.connector.connect(
	  host=host,
	  user=user,
	  passwd=password
	)

	return mydb

# Create databases
def Create_database(mydb, accounts_to_add):
	mycursor = mydb.cursor()

	for acc_name in accounts_to_add:

		mycursor.execute("CREATE DATABASE " + acc_name)

# Setups up the database
def setup_database(path_db, path_acc):

	# Get the database data
	host, user, password = read_database_data(path_db)

	#Account names
	account_info = read_account_data(path_acc)

	# Connect and get mydb from database
	mydb = connect_db(host, user, password)
	
	# Get the accounts missing databases
	accounts_to_add = exists_database(account_info.keys(), mydb)

	# Create these databases
	Create_database(mydb, accounts_to_add)
	


