import requests
import time
import csv

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup as bs

def scrape(driver, sbd): #takes the driver and the subdomain for concats as params
	html = driver.page_source
	soup = bs(html, "html.parser")
#The current page number
#page = soup.find('li', class_='current').text.strip()[5:7]
	allBooks = soup.find_all('article', class_='product_pod')

	with open("allBooks.csv", "a") as dump: #Open the csv file to write the data to
		writer = csv.writer(dump)

		for book in allBooks: #Loop through each 'article', extract info, write to csv file
#Encoding: .replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u'\u201c', '"').replace(u'\u201d', '"')
			title = book.find('h3').find('a').get('title').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u'\u201c', '"').replace(u'\u201d', '"').replace(u'\xe1',' ').replace(u'\xe9',' ')
			infoUrl = sbd + book.find('div', class_='image_container').find('a').get('href')
			price = "$" + book.find('p', class_='price_color').text.strip().encode('ascii','ignore').decode('ascii')
			ifAvailable = book.find('p', class_='instock').text.strip().encode('ascii','ignore').decode('ascii')
			coverUrl = sbd + book.find('div', class_='image_container').find('a').find('img').get('src')
			rating = book.find('p', class_='star-rating').get('class')[1]

			writer.writerow([title,infoUrl,price,ifAvailable,coverUrl,rating])
			
			

	driver.find_element_by_link_text('next').click() #Move to next page after scraping the current one and writing to csv






#PATH TO WEBDRIVER
path = 'path/to/webdriver'

#ORIGIN URL
url = "http://books.toscrape.com/"

#THE PAGE NUMBER TO STOP
toStop = 50
currentPage = 0

#RUN DRIVER
driver = webdriver.Chrome(path)
driver.get(url)

#RUN FROM FIRST TO LAST PAGE
while (currentPage < toStop):
	scrape(driver, url)
	currentPage+=1

time.sleep(3)
driver.quit()

