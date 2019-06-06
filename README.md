# Instagram
Contains crawler, downloader, storing in database, statistics and uploader/automation

## 1. Crawler: Start with the crawler which scrapes each instagram page contained in the txt file for: 
	
	```text
	Will be a module with different function for each command:

	- The amount of posts
	- The number of followers
	- The amount followed
	- The amount of likes in the last **i** photos/videos starting with the latest where **i** is a input integer
	- The amount of comments in the last 'j' photos/videos starting with the latest where 'j' is a input integer
	- The text of all comments in the last 'k' photos/videos starting with the latest where 'k' is a input integer
	- The description text of each 'l' images checked where 'l' is a input integer
	- The href link to the 'm' photos/videos in question, where 'm' is a input integer

	Where i, j, k, l, m were used as placeholders to show that they can be independent.
	```

## 2. Downloader: downloads all of the href links specified
	


## 3. Storing in a database: after each different scrape function may have run, choose if need to update or insert into sql database.



## 4. Statistics: Simple mean value of the amount of comments/amount of posts etc to better provide a good scoring system.	



## 5. Uploader/Automation: Take the new images/videos and upload the images by the specified time slots per day.



### Example use:
	
	Grab 'kittenattackz' from accounts.txt and proceed to check if 'kittenattackz' exists in the database. If not, then proceeds to check the amount of posts, the amount of followers, the amount of likes in all photos/videos, the amount of comments in all photos/videos inputs each of these in the table created for 'kittenattackz' in the database.

	If 'kittenattackz' exists already in the database then check if the amount of posts have increased and then check the amount of images/videos that the amount of posts increased by for The amount of likes, The amount of comments, The text of all comments, The description text of all images/videos and The href links and also the amount of followers.

	Score the images/videos according to the ratio between (likes + comments*X)/followers, where X is some function derived from the ratio of likes and comments (or the importance of comments for the top ratio photos/videos).

	Download the images/videos

	Store all relevant new data in the database.





There should be no need for a user to check the database manually or manually enter the data.

	This makes it so that there's no need to check further than if the amount of posts increased for a user or not.