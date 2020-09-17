
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import os
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(2)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('ul', class_='item_list')

    for article in articles:
        title = article.find('div', class_='content_title').text
        news_p = article.find('div', class_= 'article_teaser_body').text
    
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    first = soup.find('img', class_= "main_image")['src']

    featured_image_url = ("https://www.jpl.nasa.gov" + first)

    
    url_3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url_3)
    df = tables[0]
    df.columns = ['Category', 'Measurements']

    table = df.to_html(index = False, classes="table table-striped")


    url_4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_4)
    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for article in articles: 
        image = article.find('img')['src']
        img_url = ('https://astrogeology.usgs.gov' + image)
        
        t = article.find('div', class_='description')
        title_2 = t.find('h3').text
        

        hemisphere_image_urls.append({"title": title_2, "img_url": img_url})

    mars_data = {
        "title": title,
        "news_p": news_p,
        "fi_url": featured_image_url,
        "stats": table,
        "h_image": hemisphere_image_urls
    }
    
    browser.quit()
    return mars_data
        