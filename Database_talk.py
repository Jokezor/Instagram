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
	
	# The tables all databases will have
	tables_tot = ['stats', 'number_posts', 'followers', 'following', 'likes', 'comments', 'comments_text', 'descriptions', 'hrefs']

	# Keeps track of tables to add
	tables_to_add = {account: [] for account in accounts}

	# Access each account's database
	for acc_name in accounts:
		mydb = connect_to_account_db(host, user, password, acc_name)

		mycursor = mydb.cursor()

		# Get the tables
		mycursor.execute("SHOW TABLES")

		# Take the tables and save in list for comparing
		tables_check = [table for table in mycursor]

		# Remove one for each already existing
		for table in tables_tot:
			if not any(table_check == table for table_check in tables_check):
				tables_to_add[acc_name].append(table)

	return tables_to_add


			
def create_table(accounts, host, user, password, tables_to_add):

	# Access each account's database
	for acc_name in accounts:
		mydb = connect_to_account_db(host, user, password, acc_name)

		for table in tables_to_add:
			mycursor = mydb.cursor()

			stats_table = "CREATE TABLE table (number_posts int, followers int, following int, mean int)"

			# Create table
			mycursor.execute(stats_table)



	


def create_tables(path_db, path_acc):
	# Get the database data
	host, user, password = init.read_database_data(path_db)

	#Account names
	accounts = init.read_account_data(path_acc)

	# Check if tables exist and get list of missing tables
	tables_to_add = check_tables(accounts, host, user, password)

	# Create the tables





