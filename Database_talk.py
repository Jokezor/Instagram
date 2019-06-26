'''
	Will contain the functions used to talk to the database.

'''

import mysql.connector
import os

# Own code
import init

# Connect to specific database
def connect_to_account_db(host, user, password, acc_name):

	mydb = mysql.connector.connect(
	  host=host,
	  database=acc_name,
	  user=user,
	  passwd=password
	)

	return mydb


def check_tables(accounts, host, user, password):
	
	
	tables_tot = ['number_posts', 'followers', 'following', 'likes', 'comments', 'comments_text', 'descriptions', 'hrefs']

	tables_to_add = {account: len(tables_tot) for account in accounts}

	# Access each account's database
	for acc_name in accounts:
		mydb = connect_to_account_db(host, user, password, acc_name)

		mycursor = mydb.cursor()

		mycursor.execute("SHOW TABLES")

		# Remove one for each already existing
		for table in mycursor:
			tables_to_add[acc_name] -= 1

		print(tables_to_add)


			


	


def create_tables(path_db, path_acc):
	# Get the database data
	host, user, password = init.read_database_data(path_db)

	#Account names
	accounts = init.read_account_data(path_acc)

	# Check if tables exist, else create them
	check_tables(accounts, host, user, password)



