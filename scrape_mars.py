
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import os
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "'chromedriver (2).exe'"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('ul', class_='item_list')

    for article in articles:
        title = article.find('div', class_='content_title').text
        news_p = article.find('div', class_= 'article_teaser_body').text
        #print('-------------')
        # print(title)
        # print(news_p)
    browser.quit()
    
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    time.sleep(2)

    for url in url_2:
        html=browser.html
        soup = BeautifulSoup(html, 'html.parser')
        buttons = soup.find('a', class_="button fancybox")

        for button in buttons:
            href = button.get('data-fancybox-href')
    #         first = href.split()[0]
    #         #image = first.pop(0)
    #         #print(first)
            featured_image_url = ("https://www.jpl.nasa.gov" + href)
            print(featured_image_url) 
    browser.quit()
    
    url_3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url_3)
    df = tables[0]
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')


    url_4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_4)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #page = soup.find('div', class_='collapsible results')

    articles = soup.find_all('div', class_='item')

    #print(articles)
    # title_list = []
    # image_list = []

    hemisphere_image_urls = []

    for article in articles: 
        image = article.find('img')['src']
        img_url = ('https://astrogeology.usgs.gov' + image)
        
        t = article.find('div', class_='description')
        title = t.find('h3').text
        
    #     image_list.append(img_url)
    #     title_list.append(title)  
        browser.quit()

        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    mars_data = {
        "News Title": title,
        "Paragraph": news_p,
        "Image 1": featured_image_url,
        "Mars Stats": df,
        "hemisphere_image": hemisphere_image_urls
    }
    return mars_data
        