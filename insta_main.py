'''
	This is the main script which will handle all of the functions of the isntagram
	scraper, bot and statistics etc.

'''

# Own code
import init
import Database_talk

# Creates all databases/tables needed for accounts.
def setup(path_db, path_acc):

	# Creates the database
	init.setup_database(path_db, path_acc)

	# Create tables for each account
	Database_talk.create_tables(path_db, path_acc)



# Second we need to call the setup.py which will talk to the database, setup if doesn't exist.



if __name__ == '__main__':

	# File with your login to database such as host, user = 'your_user' and pass = 'your_password' (Need single quotes)
	path_db = '../database_info/database_info.txt'

	# Contains the name of your account which will be used to create db.
	path_acc = '../account_info/account_info.txt'

	# First we need to create the database which we will use to handle all the data
	setup(path_db, path_acc)