'''
	Will contain the functions used to talk to the database.

'''

import mysql.connector
import os

# Own code
import init

# Connect to specific database with account name
def connect_to_account_db(host, user, password, acc_name):

	mydb = mysql.connector.connect(
	  host=host,
	  database=acc_name,
	  user=user,
	  passwd=password
	)

	return mydb


def get_table_queries():

	stats_query = "CREATE TABLE %s (theme varchar(255), number_posts int, followers int, following int, mean_likes int, mean_comments int, mean_scores int)" %('stats')
	media_query = "CREATE TABLE %s (href varchar(255), likes int, comments int, comments_text varchar(5000), descriptions varchar(5000))" %('media')

	table_queries = {'stats': stats_query, 'media': media_query}

	return table_queries


# Creates the table if it doesn't exist
def create_table(account_info, host, user, password, table_queries):

	# Access each account's database
	for acc_name in account_info.keys():
		mydb = connect_to_account_db(host, user, password, acc_name)

		for table_query in table_queries.values():
			mycursor = mydb.cursor()

			# Create table
			try:
				mycursor.execute(table_query)
			except:
				print("Already existing tables.")
			else:
				print("Created new table for account: %s" %acc_name)


# Gets the path of database and account text files and creates tables if not existing.
def create_tables(path_db, path_acc):
	# Get the database data
	host, user, password = init.read_database_data(path_db)

	#Account names
	account_info = init.read_account_data(path_acc)

	# Gets queries
	table_queries = get_table_queries()
	
	# Create the tables
	create_table(account_info, host, user, password, table_queries)

	

# Insert init data into the tables
def insert_init_values(path_db, path_acc):

	host, user, password = init.read_database_data(path_db)

	# Account names
	account_info = init.read_account_data(path_acc)

#theme varchar(255), number_posts int, followers int, following int, mean_likes int, mean_comments int, mean_scores int
	for acc_name in account_info.keys():
		mydb = connect_to_account_db(host, user, password, acc_name)

		# Insert into theme query, next time, check if this works.
		insert_query = "INSERT INTO %s (theme, number_posts, followers, following, mean_likes, mean_comments, mean_scores)\n Values (%s, 0, 0, 0, 0, 0, 0)" % (acc_name, account_info[acc_name])




	

	




