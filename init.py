'''
	Used to iniate the database
'''

import mysql.connector
import os

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

	# Remove extra stuff
	for i in range(0, len(accounts)):
		accounts[i] = accounts[i].split('\'')[1]



	# close file
	acc_file.close()

	return accounts

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
	accounts = read_account_data(path_acc)

	# Connect and get mydb from database
	mydb = connect_db(host, user, password)
	
	# Get the accounts missing databases
	accounts_to_add = exists_database(accounts, mydb)

	# Create these databases
	Create_database(mydb, accounts_to_add)
	


