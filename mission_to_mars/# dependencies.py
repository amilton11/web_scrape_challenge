# dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

# def scrape all functions into a scrape
def scrape():

    data = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Assign the variables
    time.sleep(2)
    html = browser.html
    soup = bs(html,'html.parser')

    top_news = soup.find('div', class_='list_text')
    title = top_news.find('div', class_='content_title')

    data["title"]= title

    #top_news = soup.find('div', class_='list_text')
    sub_title = top_news.find('div', class_='article_teaser_body')

    data["sub_title"]= sub_title

    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")

    soup.find("a", class_="fancybox-thumbs")

    image = soup.find("a", class_="fancybox-thumbs")["href"]
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image
    data["image_url"]= featured_image_url

    fact_url = "https://space-facts.com/mars/"
    browser.visit(fact_url)
    mars_data = pd.read_html(fact_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    data["mars_facts"]= mars_facts

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")

    img_list = soup.find_all('a', class_="product-item")
    link_list = []

    for images in img_list:
        link_list.append(images["href"])
        
    hemispheres = set(link_list)

    mars_hemisphere = []


    for hemisphere in hemispheres:   
        browser.visit('https://astrogeology.usgs.gov'+ hemisphere)
        html = browser.html
        soup=bs(html, "html.parser")

        title = soup.title.text
        
        for link in soup.find_all('a'):
        
            if link.text == "Sample":
                image_url = link['href']
            
        mars_hemisphere.append({"title": title, "img_url": image_url})
    data["mars_hemisphere"]= mars_hemisphere

# destroy browser
    browser.quit()

    # return data as a dictionary
    return data 