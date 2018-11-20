
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import time

def url_addr(i):
# URL Dictionary Menu:
# 1: NASA Mars News
# 2: JPL Mars Space Images - Featured Image
# 3: Mars Weather
# 4: Mars Facts
# 5: Mars Hemispheres
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
    browser.visit(url_addr[i])
    print(url_addr[i])
    # Create BeautifulSoup object; parse with html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return soup, browser, url_addr[i]

# ### NASA Mars News
# Retrieve 'NASA Mars News' page with splinter module
def nasa_mars_news():
    #browser = open_Chrome()
    #browser.visit(url[1])
    #print(url[1])

    # Create BeautifulSoup object; parse with html
    #html = browser.html
    #soup = BeautifulSoup(html, 'html.parser')
    soup, browser = createSoup(1)
    # Extract title text
    title = soup.title.text
    print(title)

    # Examine the results, then determine element that contains news info
    # results are returned as an iterable list
    nasa_mars_news = []
    results = soup.find_all('div', class_="image_and_description_container")
    for result in results:
        mars_news = {}
        news_link=result.find('a')
        #print(news_link.text)
        news_summary=news_link.find('div', class_="rollover_description_inner").text.strip('\n')
        try:
            news_title=news_link.h3.text
        # When H3 tag not available then use Alt tag
        except AttributeError:
            news_title_img=news_link.find_all('img',alt=True)
            news_title=news_title_img[1]['alt'] 
        mars_news[news_title]=news_summary
        nasa_mars_news.append(mars_news)
    print(nasa_mars_news)
    browser.quit()
    return nasa_mars_news
    


# ### JPL Mars Space Images - Featured Image
# Retrieve 'JPL Mars Space Images - Featured Image' page with splinter module
def nasa_mars_feature_image():
    soup, browser = createSoup(2)
    time.sleep(1)
    print(soup.find('footer'))
    browser.click_link_by_id('full_image')
    # See if browser went to new/next html page
    soup=BeautifulSoup(browser.html,'html.parser')
    print(soup.find_all('a', class_='button'))
    try:
        time.sleep(5)
        browser.click_link_by_partial_text('more info')
        print('clicked more info button')
    except:
        time.sleep(5)
        browser.click_link_by_partial_href('/spaceimages/details.php?id=')
        print('clicked href link')

    browser.click_link_by_partial_href('/spaceimages/images/largesize')

    nasa_mars_featured_image_url=browser.url
    print(nasa_mars_featured_image_url)
    # (Re)Create dict()
    nasa_mars_featured_image={}
    nasa_mars_featured_image["nasa_mars_featured_image_url"]=nasa_mars_featured_image_url
    print(nasa_mars_featured_image)
    browser.quit()
    return nasa_mars_featured_image

# ### Mars Weather
# Retrieve 'Mars Weather' twitter page with splinter module
def nasa_mars_weather():
    soup, browser = createSoup(3)
    time.sleep(1)

    # Scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`.
    # Get first Top tweet on twitter page
    try:
        mars_weather = soup.find('div', class_="js-tweet-text-container").p.text
    except:
        time.sleep(1)
        mars_weather = soup.find('div', class_="js-tweet-text-container").p.text
        print('Worked on second try!')
    print(mars_weather)
    twitter_mars_weather={}
    twitter_mars_weather["mars_weather"]=mars_weather
    print(twitter_mars_weather)
    browser.quit()
    return twitter_mars_weather

# ### Mars Facts
# Retrieve 'Mars Facts' table with pandas module
# Convert list to DataFrame then to html table
def nasa_mars_facts_table():
    import pandas as pd
    mars_space_facts_url = url_addr[4]
    # Read into table into list
    tables = pd.read_html(mars_space_facts_url)
    # Convert to Dataframe
    df=tables[0]
    df.columns=['Metric','Measurement']
    df.set_index('Metric',inplace=True)
    df.index
    nasa_mars_facts_html_table = df.to_html()
    nasa_mars_facts_html_table=nasa_mars_facts_html_table.replace('\n', '')
    df.to_html('mars_facts_table.html')

# ### Mars Hemispheres
# Retrieve 'Mars Hemispheres' page with splinter module
def nasa_mars_hemisphere():
    soup, browser, url = createSoup(5)
    time.sleep(1)

    # Obtain high resolution images for each of Mar's hemispheres.
    # Navigate the site and find then click each of the links to the hemispheres in 
    # order to find the image url to the full resolution image.
    results = soup.find_all('div', class_="item")
    nasa_mars_hemisphere_image_urls=[]
    for result in results:
        title_image_url={}
        href_string=result.find('div',class_='description').a.string
        print(href_string)
        title_image_url['title']=href_string
        try:
            browser.click_link_by_partial_text(href_string)
            html=browser.html
            soup=BeautifulSoup(html, 'html.parser')
            download_url=soup.find_all('div',class_='downloads')
            #print(download_url)
            for download in download_url:
                #print(download.find('a').text)
                image_url=download.a['href']
                print(image_url)
                title_image_url['image_url']=image_url
            nasa_mars_hemisphere_image_urls.append(title_image_url)
            # Go back to initial page with splinter module to click on next div item
            browser.visit(url)
        except ElementDoesNotExist:
            print("Scraping Complete")
        print(nasa_mars_hemisphere_image_urls)
    browser.quit()
    return nasa_mars_hemisphere_image_urls
  


    


# ## Step 2 - MongoDB and Flask Application

# In[54]:


# Establish a connection to MongoDB with PyMongo you use the MongoClient class
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[55]:


# create a database object referencing a new database, called 'nasa_mars_landing_db'
db = client.nasa_mars_landing_db


# In[56]:


# List of dictionaries and assigned variables from above:
#print(nasa_mars_featured_image_url)
#print(mars_weather)
#print(html_table)
#print(nasa_mars_hemisphere_image_urls)
#print(nasa_mars_news)


# ### JPL Mars Space Images - Featured Image

# In[57]:


# Drop/Create 'table_nasa_mars_featured_image'
# then insert 'nasa_mars_featured_image' into database document collections table
db.table_nasa_mars_featured_image.drop()
db.table_nasa_mars_featured_image.insert_one(nasa_mars_featured_image)


# In[61]:


print(list(db.table_nasa_mars_featured_image.find()))


# ### Mars Weather

# In[59]:


# Drop/Create 'table_twitter_mars_weather'
# then insert 'twitter_mars_weather' into database document collections table
db.table_twitter_mars_weather.drop()
db.table_twitter_mars_weather.insert_one(twitter_mars_weather)


# In[60]:


print(list(db.table_twitter_mars_weather.find()))


# ### Mars Facts

# In[62]:


db.table_mars_facts.drop()
db.table_mars_facts.insert_one(mars_facts)


# In[63]:


print(list(db.table_mars_facts.find()))


# ### Mars Hemispheres

# In[64]:


# Drop/Create 'table_nasa_mars_hemisphere_image_urls'
# then insert 'nasa_mars_hemisphere_image_urls' into database document collections table
db.table_nasa_mars_hemisphere_image_urls.drop()
db.table_nasa_mars_hemisphere_image_urls.insert_many(nasa_mars_hemisphere_image_urls)


# In[65]:


print(list(db.table_nasa_mars_hemisphere_image_urls.find()))


# ### NASA Mars News

# In[66]:


# Drop/Create 'table_nasa_news' (if it does not exist) then insert 'nasa_mars_news' 
# into database document collections table
db.table_nasa_mars_news.drop()
db.table_nasa_mars_news.insert_many(nasa_mars_news)


# In[67]:


print(list(db.table_nasa_mars_news.find()))


# In[74]:


print(db.list_collection_names())


# In[69]:


print(client.list_database_names())


# In[70]:


if 'nasa_mars_landing_db' in client.list_database_names():
  print("The database exists.")


# In[75]:


#get_ipython().system('jupyter nbconvert --to=python mission_to_mars-Copy1.ipynb')

