import scrapy
import csv
from selenium import webdriver

class AngularSpider(scrapy.Spider):
	name = 'angular_spider'
	start_urls = [
		'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
	]    
	# Initalize the webdriver    
	def __init__(self):
		self.driver = webdriver.Chrome()


	# Parse through each Start URLs
	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url=url, callback=self.parse)    


	# Parse function: Scrape the webpage and store it
	def parse(self, response):
		self.driver.get(response.url)
		# Output filename
		filename = "angular_data.csv"
		with open(filename, 'a+') as f:
			writer = csv.writer(f)
			print(type(response.body))
			# Selector for all the names from the link with class 'ng-binding'
			#f.write(response.body)
			self.log('Saved file %s' % filename) 