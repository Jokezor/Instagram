# This program will scrape a set of instagram pages for the top 3 posts and calculate the ratio of impressions vs followers

# import libraries
# coding: latin-1
from urllib.request import urlopen
import sys
from bs4 import BeautifulSoup
import requests
import re
import string
import numpy as np
#from requests.auth import HTTPDigestAuth
import json
import ssl
import operator
from operator import itemgetter
import selenium.webdriver as webdriver
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

# Get all instagram pages
mainlist = []
infile = open('test.txt','r')
for line in infile:
    mainlist.append(line.strip().split(','))

infile.close()
Pages = mainlist[0]


Starthtml = "https://www.instagram.com/"
# Number of pages to loop
n=len(Pages)
Followers = [];
print(n)

# Number of images/videos
m=12
ImageLinks = [];
Likes = [];
Comments = [];
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome('/anaconda/lib/python3.6/chromedriver', chrome_options=chromeOptions)


for i in range(0,n):

    # One for each page
    ImageLinks.append([])
    Likes.append([])
    Comments.append([])

    # Counts amount of images/videos
    k=0
    # To get the page to get
    quote_page=Starthtml+Pages[i]
    page = urlopen(quote_page)
    driver.get(quote_page)

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html5lib')
    # This is with Selenium, needed for amount of likes etc.
    soup_1 = BeautifulSoup(driver.page_source,'html5lib')

    # Get the number of Followers
    Followlink = soup.find("meta",{"name":"description"})
    Followers.append(str(Followlink));
    Followers[i]=Followers[i].split('F')[0]


    # Checks if there's millions or thousands of followers
    if Followers[i].find("m ") != -1:
        Followers[i]=float(re.sub("[^0-9^.]", "",Followers[i]))*1000000
    elif Followers[i].find("k ") != -1:
        Followers[i]=float(re.sub("[^0-9^.]", "",Followers[i]))*1000
    else:
        Followers[i]=float(re.sub("[^0-9^.]", "",Followers[i]))



    # Get the links to all the 12-24 images/videos
    basesite = 'https://www.instagram.com'
    '''
    for x in soup_1.find_all('div', {'class':'_mck9w _gvoze _tn0ps'}):
        ImageLinks[i].append(basesite+x.find('a')['href'])
        k=k+1
    '''
    dr=0
    X = soup_1.find_all('div', {'class':"Nnq7C weEfm"})

    # get the 12-24 first Imagelinks
    for i in range(0,len(X)):
        for y in X[i].find_all("a", href=True):
            print (y['href'])

    #for x in soup_1.find_all('div', {'class':"Nnq7C weEfm"}):
        #print(x.find('a')['href'])
    #    print(x.find_all('div', {'class':"v1Nh3 kIKUG  _bz0w"}))
        #for y in x.find_all('a'):
        #    print(y.find('a')['href'])


        #for tag in li:
        #    for i in tag.find_all("div", {"class": "name"}):
    #print(b.find_all('a')['href'])
    #for x in soup_1.find_all('div', {'class':'v1Nh3 kIKUG  _bz0w'}):
        #print(x.find('a')['href'])
    #    ImageLinks[i].append(basesite+x.find('a')['href'])
    #    k=k+1
    #print (x.find_all('a')[0])
    #print(ImageLinks)

    # Now we need to find the likes and comments to these
'''
    for m in range(0,k):
        # Need to parse every page :/
        driver.get(ImageLinks[i][m])
        Engagesoup = BeautifulSoup(driver.page_source,'html5lib')
        EngageLink=Engagesoup.find("meta",{"property":"og:description"})
        Likes[i].append(str(EngageLink))
        Comments[i].append(str(EngageLink))

        # Splits at "Likes"
        Likes[i][m]=Likes[i][m].split('L')[0]


        # Checks if there's millions, thousands or hundreds of likes
        if Likes[i][m].find("m ") != -1:
            Likes[i][m]=float(re.sub("[^0-9^.]", "",Likes[i][m]))*1000000
        elif Likes[i][m].find("k ") != -1:
            Likes[i][m]=float(re.sub("[^0-9^.]", "",Likes[i][m]))*1000
        else:
            Likes[i][m]=float(re.sub("[^0-9^.]", "",Likes[i][m]))

        # Split at "Comments"
        Comments[i][m]=Comments[i][m].split('C')[0]
        # Split at "Likes"
        Comments[i][m]=Comments[i][m].rsplit('s', 1)[1]

        # Check if there's millions, thousands or hundreds of comments
        if Comments[i][m].find("m ") != -1:
            Comments[i][m]=float(re.sub("[^0-9^.]", "",Comments[i][m]))*1000000*6
        elif Comments[i][m].find("k ") != -1:
            Comments[i][m]=float(re.sub("[^0-9^.]", "",Comments[i][m]))*1000*6
        else:
            Comments[i][m]=float(re.sub("[^0-9^.]", "",Comments[i][m]))*6


#print(Followers)
#print(Likes)
#print(Comments)
driver.close()

ratio = [];
best_ratio = [];


# Now we got the Followers, Likes and Comments (Ignoring views)
# Time to calculate ratio. (Likes+Comments)/Followers

# i is for all the pages to view, k is the total number of pages to look through



for i in range(0,n):
    ratio.append([])
    best_ratio.append([])
    for j in range(0,m):
        ratio[i].append(float((Likes[i][j]+Comments[i][j])/Followers[i]))
    index, value = max(enumerate(ratio[i]), key=operator.itemgetter(1))

    best_ratio[i].append(ImageLinks[i][index])
    best_ratio[i].append(value)

best_ratio=sorted(best_ratio, key = operator.itemgetter(1), reverse=True)

print(best_ratio)
'''
driver.quit()
