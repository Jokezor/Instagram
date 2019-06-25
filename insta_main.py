'''
	This is the main script which will handle all of the functions of the isntagram
	scraper, bot and statistics etc.

'''

# First we need to create the database which we will use to handle all the data
import init

def setup():

	# Creates the database
	init.setup_database()


# Second we need to call the setup.py which will talk to the database, setup if doesn't exist.



if __name__ == '__main__':
	setup()