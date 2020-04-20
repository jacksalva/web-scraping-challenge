import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    # News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    results = soup.body.find('div', class_='list_text')
    news_title = results.find("div", class_="content_title").text
    news_text = results.find("div", class_ ="article_teaser_body").text
    mars_dict['news_title'] = news_title
    mars_dict['news_text'] = news_text

    #Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    image_search = soup.find('article', class_='carousel_item')
    featured_image_url = 'https://www.jpl.nasa.gov' + image_search['style'].split("'")[1]
    mars_dict['featured_image'] = featured_image_url

    #Twitter
    url = "https://twitter.com/marswxreport?lang=en"
    request = requests.get(url)

    soup = BeautifulSoup(request.text, 'html.parser')
    mars_weather = soup.find('div', class_="js-tweet-text-container").text
    mars_dict['mars_weather'] = mars_weather

    #Pandas
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    html_table = tables[0].to_html()
    mars_dict['mars_table'] = html_table

    #Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    driver = webdriver.Chrome()

    soup = BeautifulSoup(browser.html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')

    hemispheres_image_urls = []
    i = 0

    for item in hemispheres:

        driver.get(url)
        link = driver.find_elements_by_xpath("//h3")[i]
        title = link.text
        link.click()

        # wait to make sure the new window is loaded
        WebDriverWait(driver, 10).until(lambda d: d.title != "")

        img = driver.find_elements_by_xpath("//li/a")[0]
        img_url = img.get_attribute('href')
    
        hemispheres_image_urls.append({"title": f'"{title}"', 'image_url':f'"{img_url}"'})
        i += 1
    mars_dict['hemispheres'] = hemispheres_image_urls

    return mars_dict