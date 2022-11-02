#import
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Web URL
url = 'https://redplanetscience.com/'
browser.visit(url)

###
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

###Variables
quotes = soup.find_all('div', class_='list_text')

###Store the results
news_results=[]

###
for article in quotes:
	title = article.find








browser.quit()

