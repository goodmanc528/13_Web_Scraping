
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests


#Function to initialize the Chrome browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


#Function that will scrape the various websites pulling down information on Mars
def scrape():
    # Initialize Chrome using init_browser function
    browser = init_browser()

    #create dictionary to store information
    marsScrape = {}

    #### NASA Mars News - Pull the latest Mars news from NASA.gov
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    # print(f'{news_title} | {news_p}') #print results



    #### JPL Mars Space Images - Pull the Mars Picture of the day
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    imageURL = soup.find('a', class_="fancybox")['data-fancybox-href']
    featured_image_url = "http://www.jpl.nasa.gov" + imageURL
    # print(featured_image_url) #print results


    #### Mars Weather - pull the Mars weather forcast from the MarsWXReport Twitter Account
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html = browser.html
    soup = bs(html, 'html.parser')
    tweetText = soup.find('p', class_='tweet-text').text
    # print(tweetText) #print results


    #### Mars Facts - Use Pandas to convert Mars Facts from the data to a HTML table string.
    url4 = 'http://space-facts.com/mars/'
    browser.visit(url4)
    html = browser.html
    table = pd.read_html(url4)
    marsTable = table[0]
    marsTable.columns = ['Property','Value']
    marsTable.set_index('Property', inplace=True)
    marsFacts = marsTable.to_html(border=0, classes="table table-striped", table_id="mars_facts")
    #marsTable.head() #print results


    #### Mars Hemispheres - Retrieve photographs of Mars' hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html = browser.html
    soup = bs(html, 'html.parser')
    marsURLS = soup.find_all('div', class_="description")
    # print(marsURLS) #Check to see if bs object built as expected
    hemisphere_image_urls = []
    #Examine each item in the marsURLS list, created with BeautifulSoup, looking for the URL to the 
    for div in marsURLS:
        if (div.a):
            if (div.a['href']):
                hemiURL = 'https://astrogeology.usgs.gov' + div.a['href']
                browser.visit(hemiURL)
                html = browser.html
                soup = bs(html, 'html.parser')
                marsHemi = soup.find('h2', class_='title').text
                marsPhoto = soup.find('div', class_='downloads').ul.li.a['href']
                hemisphere_image_urls.append({'title': marsHemi,'img_url': marsPhoto})

    #print(hemisphere_image_urls) #print results

    #Store all collected data into a dictionary.
    marsScrape = {
        'Mars News Title':news_title,
        'Mars News':news_p,
        'Mars Featured Image': featured_image_url,
        'Mars Weather': tweetText,
        'Mars Facts': marsFacts,
        'Mars Hemispheres': hemisphere_image_urls
    }
    return marsScrape
