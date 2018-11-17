
# coding: utf-8

# In[71]:


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import time


# In[3]:


def exec_path():
    executable_path = {'executable_path': '\\Users\\Paul-DS\\Downloads\\chromedriver.exe'}
    return executable_path


# In[4]:


def open_Chrome():
    browser = Browser('chrome', **exec_path(), headless=False)
    return browser


# In[ ]:


# URL Dictionary Menu:
# 1: NASA Mars News
# 2: JPL Mars Space Images - Featured Image
# 3: Mars Weather
# 4: Mars Facts
# 5: Mars Hemispheres


# In[5]:


url = {
    1: 'https://mars.nasa.gov/news/',
    2: 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
    3: 'https://twitter.com/marswxreport?lang=en',
    4: 'https://space-facts.com/mars/',
    5: 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
}


# ### NASA Mars News

# In[511]:


browser = open_Chrome()
print(url[1])
# Retrieve 'NASA Mars News' page with splinter module
browser.visit(url[1])

# Create BeautifulSoup object; parse with html
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[281]:


# Extract title text
title = soup.title.text
print(title)


# In[284]:


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
    except AttributeError:  # When H3 tag not available then use Alt tag
        news_title_img=news_link.find_all('img',alt=True)
        news_title=news_title_img[1]['alt'] 
    mars_news[news_title]=news_summary
    nasa_mars_news.append(mars_news)

browser.quit()


# In[285]:


nasa_mars_news


# In[ ]:


browser.quit()


# ### JPL Mars Space Images - Featured Image

# In[16]:


browser = open_Chrome()
print(url[2])
# Retrieve 'JPL Mars Space Images - Featured Image' page with splinter module
browser.visit(url[2])

# Create BeautifulSoup object; parse with html
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[17]:


soup.find('footer')


# In[ ]:


browser.click_link_by_id('full_image')


# In[514]:


soup=BeautifulSoup(browser.html,'html.parser')


# In[515]:


soup.find_all('a', class_='button')

# In[516]:
try:
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    print('clicked more info button')
except:
    time.sleep(5)
    browser.click_link_by_partial_href('/spaceimages/details.php?id=')
    print('clicked href link')


# In[517]:


browser.click_link_by_partial_href('/spaceimages/images/largesize')


# In[518]:


featured_image_url=browser.url
print(featured_image_url)


# In[519]:


browser.quit()


# ### Mars Weather

# In[520]:


browser = open_Chrome()
print(url[3])
# Retrieve 'Mars Weather' twitter page with splinter module
browser.visit(url[3])

# Create BeautifulSoup object; parse with html
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[521]:


# Scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable called `mars_weather`.

# Get first Top tweet on twitter page
mars_weather = soup.find('div', class_="js-tweet-text-container").p.text
print(mars_weather)


# In[522]:


browser.quit()


# ### Mars Hemispheres

# In[524]:


browser = open_Chrome()
print(url[5])
# Retrieve 'Mars Hemispheres' page with splinter module
browser.visit(url[5])
time.sleep(5)
# Create BeautifulSoup object; parse with html
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[244]:


# Obtain high resolution images for each of Mar's hemispheres.

# Navigate the site and find then click each of the links to the hemispheres in 
# order to find the image url to the full resolution image.
results = soup.find_all('div', class_="item")
nasa_mars_hemisphere_image_urls=[]
for result in results:
    title_image_url={}
    href_string=result.find('div',class_='description').a.string
    print(href_string)
    browser.click_link_by_partial_text(href_string)
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    download_url=soup.find_all('div',class_='downloads')
    #print(download_url)
    for download in download_url:
        #print(download.find('a').text)
        image_url=download.a['href']
        print(image_url)
    title_image_url['title']=href_string
    title_image_url['image_url']=image_url
    nasa_mars_hemisphere_image_urls.append(title_image_url)
    # Go back to initial page with splinter module to click on next div item
    time.sleep(1)
    browser.visit(url[5])
browser.quit()
print(nasa_mars_hemisphere_image_urls)


# ### Mars Facts

# In[18]:


import pandas as pd


# In[19]:


mars_space_facts_url = url[4]


# In[20]:


tables = pd.read_html(mars_space_facts_url)
tables


# In[21]:


type(tables)


# In[22]:


df=tables[0]
df.columns=['Metric','Measurement']
df


# In[172]:


# Convert DataFrame to Dictionary for MongoDB
mars_fact_table={}
mars_fact_table['df']=df


# In[185]:


mars_fact_table


# In[23]:


df.set_index('Metric',inplace=True)


# In[24]:


df.index


# In[151]:


df.T.to_dict('records')


# In[ ]:


# NOTE: Now Insert DataFrame into MongoDB before converting to HTML! 


# In[54]:


mars_facts_dict_index=df.to_dict('index')


# In[40]:


mars_facts_dict_index


# In[74]:


mars_facts_dict=df.to_dict()
mars_facts_dict


# In[168]:


df.T.to_json()


# In[25]:


html_table = df.to_html()
html_table


# In[26]:


html_table=html_table.replace('\n', '')


# In[27]:


html_table

mars_fact_html_table={}

mars_fact_html_table["html_table"]=html_table
# In[169]:


type(html_table)


# In[28]:


df.to_html('table.html')


# ## Step 2 - MongoDB and Flask Application

# In[31]:


# Establish a connection to MongoDB with PyMongo you use the MongoClient class
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[32]:


# create a database object referencing a new database, called 'nasa_mars_landing_db'
db = client.nasa_mars_landing_db


# In[ ]:


# List of dictionaries and assigned variables from above:
print(nasa_mars_hemisphere_image_urls)

print(mars_weather)
print(featured_image_url)
print(nasa_mars_news)


# In[ ]:

print(mars_fact_html_table)
db.table_mars_facts_html.drop()
db.table_mars_facts_html.insert_one(mars_fact_html_table)


# In[159]:


list(db.table_mars_facts_html.find())


# In[ ]:


#table_nasa_mars_hemisphere_image_urls = db.nasa_mars_hemisphere_image_urls


# In[260]:


# Create 'table_nasa_mars_hemisphere_image_urls' (if it does not exist) 
# then insert 'nasa_mars_hemisphere_image_urls' into database table
db.table_nasa_mars_hemisphere_image_urls.insert_many(nasa_mars_hemisphere_image_urls)


# In[261]:


nasa=db.table_nasa_mars_hemisphere_image_urls.find()


# In[262]:


list(nasa)


# In[286]:


#table_nasa_news = db.nasa_news


# In[287]:


# Create 'table_nasa_news' (if it does not exist) then insert 'nasa_news' into database table
db.table_nasa_news.insert_many(nasa_mars_news)


# In[288]:


nasa_news_list=db.table_nasa_news.find()


# In[289]:


list(nasa_news_list)


# In[33]:


db.list_collection_names()


# In[34]:


client.list_database_names()


# In[35]:


if 'nasa_mars_landing_db' in client.list_database_names():
  print("The database exists.")


# In[ ]:


notes='''Insert a Pandas Dataframe into mongodb using PyMongo
            Here you have the very quickest way. Using the insert_many method from pymongo 3 and 'records' parameter of to_dict method.
            ->db.insert_many(df.to_dict('records'))
        
'''


# In[ ]:


#get_ipython().system('ipython nbconvert --to=python mission_to_mars-.ipynb')

