from email import header
from operator import index
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title and paragraph 
    
    news_title = soup.find('div', class_= 'content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    

    # Get the featured image 
    space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(space_image_url)
    image_html = browser.html
    soup = bs(image_html, 'html.parser')
    image =soup.find("img", class_="headerimage")
    featured_image_url = "https://spaceimages-mars.com/" + image['src']
    
    # Get the table 
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    table_html = browser.html
    soup = bs(table_html, 'html.parser')
    df = pd.read_html(facts_url)
    facts_table = df[0]
    facts_table.columns =['Description', 'Mars', 'Earth']
    facts_table["Description"] = facts_table["Description"].str.replace(":","")
    facts_table = facts_table.iloc[1: , :]
    table = facts_table.to_html(index=False,header=False, classes = "table table-sm table-striped" )

# get the Mars Hemispheres 
    marshemispheres_url = 'https://marshemispheres.com/'
    browser.visit(marshemispheres_url)
    marshemispheres_html = browser.html
    soup = bs(marshemispheres_html, 'html.parser')
    divs =soup.find_all("div", class_="item")
    hemisphere_image_urls = []


# --- use splinter's browser to click on each hemisphere's link in order to retrieve image data ---
    for hemisphere in range(len(divs)):
        hemisphere_link = browser.find_by_css('a.product-item h3')
        hemisphere_link[hemisphere].click()
        time.sleep(1)
    
    # --- create a beautiful soup object with the image detail page's html ---
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
    
    # --- create the base url for the fullsize image link ---
        base_url = 'https://marshemispheres.com/'
    
    # --- retrieve the full-res image url and save into a variable ---
        hem_url = image_soup.find('img', class_="wide-image")['src']
    
    # --- complete the featured image url by adding the base url ---
        img_url = base_url + hem_url

    # --- retrieve the image title using the title class and save into variable ---
        img_title = browser.find_by_css('.title').text
        hemisphere_image_urls.append({"title": img_title,
                              "img_url": img_url})
    
    # --- go back to the main page ---
        browser.back()
    
# --- close the browser session ---    

    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "mars_img": featured_image_url,
        "news_title": news_title,
        "news_p": news_p, 
        "table": table, 
        "hemisphere_images": hemisphere_image_urls

    }   

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
