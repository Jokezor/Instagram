import datetime
from time import sleep
import selenium


# Try and locate if the account is private and if so return 1, return 0 otherwise.
def is_Private_account(selenium_object):

	# May need to update this in future.
	private_class = 'rkEop'
	# Try to check if this class is available and if so if the message matches the private_status message.
	private_status = 'This Account is Private'

	try:
		# Get the status message, returns list of selenium objects
		status_message = selenium_object.driver.find_elements_by_class_name(private_class)

		# If the message reads private, then assume private
		if status_message:
			if status_message[0].text == private_status:
				return 1
	except selenium.common.exceptions.NoSuchElementException:
		return 0




# Gets and returns the nr_posts, number of followers and number of following
def Get_Basic_stats(selenium_object, response):
	
	# Will need to update this as time goes on.
	base_stats_class = 'g47SY'

	# Get's the nr_posts, Followers and Following in one list.
	Basic_stats = selenium_object.driver.find_elements_by_class_name(base_stats_class)

	# Access the metrics
	number_posts = Basic_stats[0].text.replace(',', '')

	# To convert from string (place in general function)
	if 'm' in number_posts:
		number_posts = int(float(number_posts.split("m")[0])*1000000)
	elif 'k' in number_posts:
		number_posts = int(float(number_posts.split("k")[0])*1000)

	Followers = Basic_stats[1].text.replace(',', '')

	if 'm' in Followers:
		Followers = int(float(Followers.split("m")[0])*1000000)
	elif 'k' in Followers:
		Followers = int(float(Followers.split("k")[0])*1000)

	Following = Basic_stats[2].text.replace(',', '')

	if 'm' in Following:
		Following = int(float(Following.split("m")[0])*1000000)
	elif 'k' in Following:
		Following = int(float(Following.split("k")[0])*1000)

	# Insert the data into the selenium object
	selenium_object.Basic_stats[response.meta['account']]['number_posts'] = number_posts
	selenium_object.Basic_stats[response.meta['account']]['Followers'] = Followers
	selenium_object.Basic_stats[response.meta['account']]['Following'] = Following

	return selenium_object

# Get the image links
def Get_Image_links(selenium_object):

	# Will need to update
	image_link_class = '_9AhH0'

	# Get's the image links
	Image_links = selenium_object.driver.find_elements_by_class_name(image_link_class)

	# If the image_link is new then append this to the Image_links.
	
	#selenium_object.Image_links[selenium_object.accounts[selenium_object.Count]] = Image_links

	return Image_links


# Get the datetime from the media
def Get_Date(selenium_object):

	# Will need to update
	date_time_class = 'time._1o9PC.Nzb55'

	# Get's datetime string and split into list
	date_time = selenium_object.driver.find_element_by_css_selector(date_time_class).get_attribute('datetime').split('-')

	# Year-Month-Day, remove time info
	date_time_string = date_time[0] + '-' + date_time[1] + '-' + date_time[2].split('T')[0]

	# Convert to datetime
	date_time_obj = datetime.datetime.strptime(date_time_string, "%Y-%m-%d")

	return date_time_obj

# Get the number of likes of image
def Get_Likes(selenium_object, response):
	
	# Will need to update
	Image_Like_class = 'Nm9Fw'
	Video_Like_class = 'vJRqr'
	Video_View_class = 'vcOH2'


	Likes = 0

	try:
		# Get likes from image
		Likes = selenium_object.driver.find_element_by_class_name(Image_Like_class).text.split(" ")[0].replace(',', '')

		if 'm' in Likes:
			Likes = int(float(Likes.split("m")[0])*1000000)
		elif 'k' in Likes:
			Likes = int(float(Likes.split("k")[0])*1000)

	except:
		# Press the views div to make likes visible
		selenium_object.driver.find_element_by_class_name(Video_View_class).click()
		sleep(0.5)

		# Get likes from video
		Likes = int(selenium_object.driver.find_element_by_class_name(Video_Like_class).text.split(" ")[0].replace(',', ''))
	
	# Likes[Account][href] = Likes
	selenium_object.Likes[response.meta['account']][selenium_object.driver.current_url] = Likes

	return selenium_object

# Need to sort out some comments. Will get the count of comments from the length of this list.
# Need to get comments if they are "hidden", sort out comments from own account.
def Get_Comments(selenium_object, response):

	# Will need to update
	Comment_class = 'C4VMK'

	# Gets the comments
	Comments = selenium_object.driver.find_elements_by_class_name(Comment_class)

	# Comments[Account][href] = []
	selenium_object.Comments[response.meta['account']][selenium_object.driver.current_url] = []

	for comment in Comments:
		selenium_object.Comments[response.meta['account']][selenium_object.driver.current_url].append(comment.text)

	return selenium_object


# Exits the media in question
def Exit_Media(selenium_object):

	# Will need to update
	Exit_Button_class = 'ckWGn'

	# Find and press the exit button
	selenium_object.driver.find_element_by_class_name(Exit_Button_class).click()


# Get's the description from the comments
def Get_Descriptions(selenium_object, response):

	# First comment of href is the description
	selenium_object.descriptions[response.meta['account']][selenium_object.driver.current_url] = selenium_object.Comments[response.meta['account']][selenium_object.driver.current_url][0]

	return selenium_object

# Get amount of comments on photo/video
def Get_num_comments(selenium_object, response):

	# Will need to update
	Comment_length_class = ''
	Comment_length = selenium_object.driver.find_elements_by_class_name(Comment_length_class).text

# Get the href
def Get_hrefs(selenium_object, response):

	# Will need to update
	xpath_hrefs = "//a[@href]" 

	pages_string = 'https://www.instagram.com/p/'

	# Get all href's currently accesible
	Hrefs = selenium_object.driver.find_elements_by_xpath(xpath_hrefs)

	for href in Hrefs:
		
		# Need to run this inside the loop and double check that
		# it's indeed the same images since we have not guarantee at the moment.
		href_string = href.get_attribute('href')

		# If the href contains the /p/ then it's a image/video.
		if pages_string in href_string:
			if href_string not in selenium_object.hrefs:
				selenium_object.hrefs[response.meta['account']].append(href_string)

	return selenium_object


#