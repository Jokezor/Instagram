from time import sleep
import datetime
import selenium
import sys

import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Own Code
sys.path.append("/Users/Newera/Documents/Instagram_non_git/Instagram/Crawlers/Instagram/spiders/")
import Scraping_functions
sys.path.append("/Users/Newera/Documents/Instagram_non_git/Instagram")
import Database_talk
import init


class QuotesSpider(Spider):
	name = "instagram"

	def start_requests(self):
	    #urls = [
	    #	"https://www.instagram.com/%s/" %self.accounts[0],
	    #	"https://www.instagram.com/%s/" %self.accounts[1],
		#]
		# First go through all the pages for all themes and then add them to the accounts which match the themes.

		# Get the total number of pages to be visited.
		# Would be good if this can be gotten as we go along. However I don't think that is possible.
		tot_length = 0
		
		for acc_name in self.accounts.keys():
			for theme in self.accounts[acc_name]:
				tot_length+=len(self.pages[theme])


		#[tot_length += len(self.pages[theme]) for theme in self.accounts[acc_name] for acc_name in self.accounts.keys()]
		#print(tot_length)

		# Get all accounts from the current_theme
		for acc_name in self.accounts.keys():
			for theme in self.accounts[acc_name]:
				for page in self.pages[theme]:
					url = "https://www.instagram.com/%s/" %page

					tot_length = len(self.accounts.keys())

					yield scrapy.Request(url, meta={'max_length':tot_length, 'account':acc_name})

	def __init__(self):
		self.driver = webdriver.Chrome()

		#options = Options()
		#options.add_argument("--disable-notifications")
		#options.add_argument("--incognito")
		#options.add_argument("--disable-extensions")
		#options.add_argument(" --disable-gpu")
		#options.add_argument(" --disable-infobars")
		#options.add_argument(" -–disable-web-security")
		#options.add_argument("--no-sandbox") 		
		#caps = options.to_capabilities()

		self.paths = init.Get_path_info()	
		
		# Number of accounts checked
		self.Count = 0

		# Get the database data
		self.host, self.user, self.password = init.read_database_data(self.paths[0])

		#Account names, keys is account names and values is the themes.
		self.accounts = init.read_account_data(self.paths[1])

		# Pages for each theme. theme: page
		self.pages = init.read_pages_data(self.paths[2])

		# 
		# Account: {}
		self.Basic_stats = {account: {'number_posts': 0, 'Followers': 0, 'Following': 0} for account in self.accounts.keys()}

		# Account: {href: likes}
		self.Likes = {account: {} for account in self.accounts.keys()}

		# Account: {href: []} (Comments as list)
		self.Comments = {account: {} for account in self.accounts.keys()}

		# Account: {href: comments[0]}
		self.descriptions = {account: {} for account in self.accounts.keys()}

		# Account: [] 
		self.hrefs = {account: [] for account in self.accounts.keys()}

		# Account: []
		self.Image_links = {account: [] for account in self.accounts.keys()}

		# Account: []
		self.checked_Image_links = {account: [] for account in self.accounts.keys()}

		# Number of media checked
		self.length_checked = {account: 0 for account in self.accounts.keys()}

		# Visited pages for each account
		self.Visited_pages = {account: [] for account in self.accounts.keys()}

		self.actions = ActionChains(self.driver)	

	def Counter(self):
		self.Count += 1

	def parse(self, response):
		
		# Access the page site
		if response.url not in self.Visited_pages[response.meta['account']]:

			# Append the page url to the list of visited pages
			self.Visited_pages[response.meta['account']].append(response.url)

			# Access the page url
			self.driver.get(response.url)

			# Check if account is private
			if not Scraping_functions.is_Private_account(self):
			
				# Get basic stats
				Scraping_functions.Get_Basic_stats(self, response)

				# Checking if we have gone back one month yet or not.
				Back_one_month = False
				#find("meta",{"property":"og:description"})
				# Short code is same as image url. Not ordered

				# Need to look through more shortcodes and edge_media_to_comment

				#print(response.xpath("//meta[@property='og:description']").extract())

				# Go through the images
				while (Back_one_month==False):

					# If checked images before, then we need to scroll in order to find new ones.
					if len((self.checked_Image_links[response.meta['account']])) > 0:
						print("\nScrolling\n")

						# 1. Scroll downwards the entire length of the page
						self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						sleep(0.2)
						self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						sleep(0.2)

						# Get the hrefs, this one is not necessary since we already get that one from the checking procedure we do.
						Scraping_functions.Get_hrefs(self, response)

						# 2. Get_Image_links and start from self.length_checked[self.accounts[self.Count]]
						# 
						# To do nr 2, we need to chop up the original Image_links,
						# Maybe include everything in a for loop to only allow ind > self.length_checked[self.accounts[self.Count]].
						# Try that first. Should be the easiest way.

						Image_links = Scraping_functions.Get_Image_links(self)

					else:
						# Get the hrefs
						Scraping_functions.Get_hrefs(self, response)

						# print(self.hrefs[self.accounts[self.Count]])

						Image_links = Scraping_functions.Get_Image_links(self)
						
					
					# Get the hrefs of these new images
					# Problem with this approach is that the href uses the index of the img_link
					# meaning that we will access the wrong href.. Instead do href:img_link pairing
					# Or getting the href when accessed the image?

					for ind, img_link in enumerate(Image_links):
						
						# Get href instead
						#if ind >= self.length_checked[self.accounts[self.Count]]:
						# Enter the image
						set_cont_0 = False
						Not_found = False
						while not set_cont_0:
							try:
								print("Clicking\n")
								img_link.click()
								set_cont_0 = True
								sleep(0.2)
							except selenium.common.exceptions.WebDriverException:
								try:
									self.actions.move_to_element(img_link).perform()
									sleep(0.2)

								except selenium.common.exceptions.StaleElementReferenceException:
									set_cont_0 = True
									Not_found = True
						
						sleep(0.2)

						# Only get the stats if the media is found
						if not Not_found:

							if self.driver.current_url not in self.checked_Image_links[response.meta['account']]:

								# Get the date of the media
								set_cont_1 = False
								while not set_cont_1:
									try:
										date_time_obj = Scraping_functions.Get_Date(self)
										if date_time_obj:
											set_cont_1 = True
									except selenium.common.exceptions.NoSuchElementException:
										sleep(0.2)

								# Call this after img_link.click() to use as href
								# Should print the href
								#print(self.driver.current_url)

								# Get Likes
								Scraping_functions.Get_Likes(self, response)

								sleep(0.2)

								# Get the comments
								Scraping_functions.Get_Comments(self, response)

								# Get descriptions
								Scraping_functions.Get_Descriptions(self, response)


								# Add the current media checked to avoid going through the same media once more.
								self.checked_Image_links[response.meta['account']].append(self.driver.current_url)

								# Finds and presses the exit button on media
								set_cont_2 = False
								while not set_cont_2:
									try:
										print("Exiting 1\n")
										Scraping_functions.Exit_Media(self)
										set_cont_2 = True
										sleep(0.2)
									except selenium.common.exceptions.NoSuchElementException:
										sleep(0.2)
								

								self.length_checked[response.meta['account']] += 1

								# Breaks the search for images if we have gone back 30 days
								print(date_time_obj)
								if (datetime.datetime.today()-date_time_obj).days >= 30:
									Back_one_month = True
									break
								
								sleep(0.2)
							else:
								set_cont_2 = False
								while not set_cont_2:
									try:
										print("Exiting 2\n")
										Scraping_functions.Exit_Media(self)
										set_cont_2 = True
										sleep(0.2)
									except selenium.common.exceptions.NoSuchElementException:
										sleep(0.2)

				# Type how far back we checked.
				print("\n\nShould be one month back now: %d days\n" %(datetime.datetime.today()-date_time_obj).days)
				print("Checked: %d images\n" %len(self.checked_Image_links[response.meta['account']]))

				# Increase count of pages checked
				self.Counter()

		
		print(self.Count)
		print(response.meta['max_length'])
		# Close driver after use, if every account's pages visited
		if self.Count >= response.meta['max_length']:
			print("Likes:")
			print(self.Likes)
			print('\n')

			print("Comments:")
			print(self.descriptions)
			print('\n')

			print("checked_Image_links:")
			print(self.checked_Image_links)
			print('\n')

			self.driver.close()





















#