# PAUL AGGARWAL 
# LINKEDIN (https://www.linkedin.com/in/paul-aggarwal-007)
# 
# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template
from flask_pymongo import MongoClient
from scrape_mars import startScraping

app = Flask(__name__)
# Establish a connection to MongoDB with PyMongo you use the MongoClient class
conn = 'mongodb://localhost:27017'
client = MongoClient(conn)
# create/connect a database object referencing a new database or existing db, called 'nasa_mars_landing_db'
db = client.nasa_mars_landing_db

@app.route('/')
def home_page():
    news = db.table_nasa_mars_news.find()
    image = db.table_nasa_mars_featured_image.find()
    weather = db.table_twitter_mars_weather.find()
    facts_html = db.table_mars_facts.find()
    image_urls = db.table_nasa_mars_hemisphere_image_urls.find()
    #print(list(image_urls))
    return render_template('index.html', news=news, image=image, weather=weather,facts_html=facts_html, image_urls=image_urls)

@app.route('/scrape')
def scrape():
    # 'startScraping' will scrape Nasa Mars website and
    # save into seperate dictionaries then insert each dictionary into
    # its own collection table inside MongoDB 'nasa_mars_landing_db'.
    #
    # NOTE: This method is different then originally planned 
    # inside READ.ME instructions where they wanted 
    # one Python dictionary containing all of the scraped data.
    # Then have this Flask app store the return value in Mongo.
    startScraping()
    # Redirect back to home page
    return redirect('/', code=302)
    
if __name__ == "__main__":
    app.run()