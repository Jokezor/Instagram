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

	# Insert information about themes into the database
	


# Second we need to call the setup.py which will talk to the database, setup if doesn't exist.



if __name__ == '__main__':

	paths = init.Get_path_info()

	path_db = paths[0]
	path_acc = paths[1]
	path_pages = paths[2]

	# First we need databases and tables to store the data
	setup(path_db, path_acc)

	# Now we can go along and start to scrape for the information we need


	#Database_talk.insert_data(path_db, path_acc)