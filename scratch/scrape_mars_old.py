# PAUL AGGARWAL 
# LINKEDIN (https://www.linkedin.com/in/paul-aggarwal-007)
# 
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import time

# Establish a connection to MongoDB with PyMongo you use the MongoClient class
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
    
def nasa_mars_db():
# create/connect a database object referencing a new database or existing db, called 'nasa_mars_landing_db'
    db = client.nasa_mars_landing_db
    return db

def url_addr(i):
# URL Dictionary Menu:
#   1: NASA Mars News
#   2: JPL Mars Space Images - Featured Image
#   3: Mars Weather
#   4: Mars Facts
#   5: Mars Hemispheres
    url = {
            1: 'https://mars.nasa.gov/news/',
            2: 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
            3: 'https://twitter.com/marswxreport?lang=en',
            4: 'https://space-facts.com/mars/',
            5: 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
            }
    return url[i]

def exec_path():
    return {'executable_path': '\\Users\\Paul-DS\\Downloads\\chromedriver.exe'}

def open_Chrome():
    return Browser('chrome', **exec_path(), headless=False)

def createSoup(i):
    browser = open_Chrome()
    url=url_addr(i)
    browser.visit(url)
    # Create BeautifulSoup object; parse with html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return soup, browser, url

# ### NASA Mars News
# Retrieve 'NASA Mars News' page with splinter module
def nasa_mars_news():
    soup, browser, first_url = createSoup(1)
    # Insert into MongoDB
    # Drop/Create 'table_nasa_mars_news' (if it does not exist)
    db=nasa_mars_db()
    db.table_nasa_mars_news.drop()
    # Examine the results, then determine element that contains news info
    # results are returned as an iterable list
    results = soup.find_all('div', class_="image_and_description_container")
    for result in results:
        nasa_mars_news = {}
        news_link=result.find('a')
        #print(news_link.text)
        news_summary=news_link.find('div', class_="rollover_description_inner").text.strip('\n')
        try:
            news_title=news_link.h3.text
        # When H3 tag not available then use Alt tag
        except AttributeError:
            news_title_img=news_link.find_all('img',alt=True)
            news_title=news_title_img[1]['alt'] 
        nasa_mars_news[news_title]=news_summary
        # Insert 'nasa_mars_news' into database document collections table
        db.table_nasa_mars_news.insert_one(nasa_mars_news)
    browser.quit()
    return db.table_nasa_mars_news
    
# ### JPL Mars Space Images - Featured Image
# Retrieve 'JPL Mars Space Images - Featured Image' page with splinter module
def nasa_mars_feature_image():
    soup, browser, first_url = createSoup(2)
    time.sleep(1)
    browser.click_link_by_id('full_image')
    try:
        time.sleep(5)
        browser.click_link_by_partial_text('more info')
    except:
        time.sleep(5)
        browser.click_link_by_partial_href('/spaceimages/details.php?id=')
    browser.click_link_by_partial_href('/spaceimages/images/largesize')
    nasa_mars_featured_image_url=browser.url
    # (Re)Create dict()
    nasa_mars_featured_image={}
    nasa_mars_featured_image["nasa_mars_featured_image_url"]=nasa_mars_featured_image_url
    # Insert into MongoDB
    # Drop/Create 'table_nasa_mars_featured_image'
    # then insert 'nasa_mars_featured_image' into database document collections table
    db=nasa_mars_db()
    db.table_nasa_mars_featured_image.drop()
    db.table_nasa_mars_featured_image.insert_one(nasa_mars_featured_image)
    browser.quit()
    return db.table_nasa_mars_featured_image

# ### Mars Weather
# Retrieve 'Mars Weather' twitter page with splinter module
def nasa_mars_weather():
    soup, browser, first_url = createSoup(3)
    time.sleep(1)
    # Scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`.
    # Get first Top tweet on twitter page
    try:
        mars_weather = soup.find('div', class_="js-tweet-text-container").p.text
    except:
        time.sleep(1)
        mars_weather = soup.find('div', class_="js-tweet-text-container").p.text
    twitter_mars_weather={}
    twitter_mars_weather["mars_weather"]=mars_weather
    # Insert into MongoDB
    # Drop/Create 'table_twitter_mars_weather'
    # then insert 'twitter_mars_weather' into database document collections table
    db=nasa_mars_db()
    db.table_twitter_mars_weather.drop()
    db.table_twitter_mars_weather.insert_one(twitter_mars_weather)
    browser.quit()
    return db.table_twitter_mars_weather

# ### Mars Facts
# Retrieve 'Mars Facts' table with pandas module
# Convert list to DataFrame then to html table
def nasa_mars_facts_table():
    import pandas as pd
    nasa_mars_space_facts_url = url_addr(4)
    nasa_mars_facts={}
    # Read into table into list
    tables = pd.read_html(nasa_mars_space_facts_url)
    # Convert to Dataframe
    df=tables[0]
    df.columns=['Metric','Measurement']
    df.set_index('Metric',inplace=True)
    df.index
    nasa_mars_facts['nasa_mars_facts_html']=df.to_html()
    #nasa_mars_facts_html_table=nasa_mars_facts_html_table.replace('\n', '')
    # Insert into MongoDB
    db=nasa_mars_db()    
    db.table_mars_facts.drop()
    db.table_mars_facts.insert_one(nasa_mars_facts)
    df.to_html('nasa_mars_facts_table.html')
    return db.table_mars_facts

# ### Mars Hemispheres
# Retrieve 'Mars Hemispheres' page with splinter module
def nasa_mars_hemisphere():
    soup, browser, first_url= createSoup(5)
    time.sleep(1)
    # Insert into MongoDB
    # Drop/Create 'table_nasa_mars_hemisphere_image_urls'
    db=nasa_mars_db()
    db.table_nasa_mars_hemisphere_image_urls.drop()
    # Obtain high resolution images for each of Mar's hemispheres.
    # Navigate the site and find then click each of the links to the hemispheres in 
    # order to find the image url to the full resolution image.
    results = soup.find_all('div', class_="item")
    #nasa_mars_hemisphere_image_urls=[]
    for result in results:
        title_image_url={}
        href_string=result.find('div',class_='description').a.string
        title_image_url['title']=href_string
        browser.click_link_by_partial_text(href_string)
        next_html=browser.html
        next_soup=BeautifulSoup(next_html, 'html.parser')
        download_url=next_soup.find_all('div',class_='downloads')
        for download in download_url:
            image_url=download.a['href']
            title_image_url['image_url']=image_url
        # Insert 'title_image_url' into database document collections table
        db.table_nasa_mars_hemisphere_image_urls.insert_one(title_image_url)
        # Go back to initial page with splinter module to click on next div item
        browser.visit(first_url)
    browser.quit()
    return db.table_nasa_mars_hemisphere_image_urls
  

# Main function
def startScraping():
    nasa_mars_hemisphere()
    nasa_mars_facts_table()
    nasa_mars_weather()
    nasa_mars_feature_image()
    nasa_mars_news()



#get_ipython().system('jupyter nbconvert --to=python mission_to_mars-Copy1.ipynb')

