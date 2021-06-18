# --- dependencies and setup ---
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #For mac users
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

    #For windows users
    # executable_path = {'executable_path': 'driver/chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # ******************************************************************************************************************************
    # Scraping Mars News
    # *****************************************************************************************************************************
    
    MarsNews_url = 'https://mars.nasa.gov/news/'

    print("Scraping Mars News...")

    # --- visit the Mars News website ---
    browser.visit(MarsNews_url)
    time.sleep(1)

    # --- create HTML object ---
    html = browser.html

    # --- parse HTML with BeautifulSoup ---
    soup = BeautifulSoup(html, 'html.parser')

    # --- get the first <li> item under <ul> list of headlines: this contains the latest news title and paragraph text ---
    first_li = soup.find('li', class_='slide')

    # --- save the news title under the <div> tag with a class of 'content_title' ---
    news_title = first_li.find('div', class_='content_title').text

    # --- save the paragraph text under the <div> tag with a class of 'article_teaser_body' ---
    news_para = first_li.find('div', class_='article_teaser_body').text

    print("Mars News: Scraping Complete!")

    # *****************************************************************************************************************************
    # Scraping JPL Featured Image URL 
    # *****************************************************************************************************************************
    
    JPLimage_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    print("Scraping JPL Featured Space Image...")

    # --- visit the JPL Featured Space Image website ---
    browser.visit(JPLimage_url)
    time.sleep(1)

    # --- create HTML object ---
    html = browser.html

    # --- parse HTML with BeautifulSoup ---
    soup = BeautifulSoup(html, 'html.parser')

    # --- get the <div> with a class of 'carousel_container': this contains the current featured image details ---
    carousel = soup.find('div', class_='carousel_container')

    # --- get the image title found under the <a> tag ---
    featuredimage_title = carousel.find('a')['data-title']

    # --- use splinter to click on the 'full image' button to retrieve a full-size jpg url ---
    browser.find_by_id('full_image').click()
    time.sleep(1)

    # --- check if the div with the 'more info' button is visible to proceed to the download page. If false: ---
    if browser.is_element_visible_by_css('div.fancybox-title') == False:
    
        # --- create the base url for the image from the carousel container ---
        base_url = 'https://www.jpl.nasa.gov/'
    
        # --- get the image url found under the <a> tag in the carousel ---
        image_url = carousel.find('a')['data-fancybox-href']
    
        # --- complete the featured image url by adding the base url ---
        featuredimage_url = base_url + image_url

    # --- if the div is visible and there is a 'more info' button to proceed --- 
    else:
    
        # --- create the base url for the fullsize image download link ---
        base_url = 'https:'
    
        # --- click the 'more info' button to go to the image detail page ---
        browser.links.find_by_partial_text('more info').click()
        time.sleep(1)
    
        # --- create a beautiful soup object with the image detail page's html ---
        img_detail_html = browser.html
        imagesoup = BeautifulSoup(img_detail_html, 'html.parser')
    
        # --- find the fullsize jpg image link and store the url ---
        download_div = imagesoup.find_all('div', class_='download_tiff')[1]
        fullsize_img = download_div.find('a')['href']

        # --- complete the featured image url by adding the base url ---
        featuredimage_url = base_url + fullsize_img

    print("JPL Featured Space Image: Scraping Complete!")

    # *****************************************************************************************************************************
    # Scraping Mars Weather Tweet
    # *****************************************************************************************************************************
    
    MarsWeather_url = 'https://twitter.com/marswxreport'

    print("Scraping Mars Weather's Twitter Account...")

    # --- visit the Mars Weather twitter account ---
    browser.visit(MarsWeather_url)
    time.sleep(5)

    # --- create HTML object ---
    html = browser.html

    # --- parse HTML with BeautifulSoup ---
    soup = BeautifulSoup(html, 'html.parser')

    # --- save the latest tweet in a variable (found in the text of the first element <span> under the <div> tag with lang="en" ---
    tweet = soup.find_all('div', lang='en')[0].text

    # --- clean up the tweet (remove newline) ---
    latest_tweet = tweet.replace('\n', '')
        
    print("Mars Weather: Scraping Complete!")

    # *****************************************************************************************************************************
    #  Scraping Mars Facts
    # *****************************************************************************************************************************
    
    MarsFacts_url = 'https://space-facts.com/mars/'

    print("Scraping Mars Facts...")

    # --- visit the Mars Facts website ---
    browser.visit(MarsFacts_url)
    time.sleep(1)

    # --- create HTML object ---
    html = browser.html

    # --- use Pandas to scrape table of facts ---
    table = pd.read_html(html)

    # --- use indexing to slice the table to a dataframe ---
    facts_df = table[0]
    facts_df.columns =['Description', 'Value']

    # --- convert the dataframe to a HTML table and pass parameters for styling ---
    html_table = facts_df.to_html(index=False, header=False, border=0, classes="table table-sm table-striped font-weight-light")

    print("Mars Facts: Scraping Complete!")

    # *****************************************************************************************************************************
    #  Scraping Mars Hemisphere images
    # *****************************************************************************************************************************
    
    MarsHemImage_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    print("Scraping Mars Hemisphere Images...")
    
    # --- visit the Mars Hemisphere website ---
    browser.visit(MarsHemImage_url)
    time.sleep(1)

    # --- create HTML object ---
    html = browser.html

    # --- parse HTML with BeautifulSoup ---
    soup = BeautifulSoup(html, 'html.parser')

    # --- retrieve all the parent div tags for each hemisphere --- 
    hemisphere_divs = soup.find_all('div', class_="item")

    # --- create an empty list to store the python dictionary ---
    hemisphere_image_data = []

    # --- loop through each div item to get hemisphere data ---
    for hemisphere in range(len(hemisphere_divs)):

        # --- use splinter's browser to click on each hemisphere's link in order to retrieve image data ---
        hem_link = browser.find_by_css("a.product-item h3")
        hem_link[hemisphere].click()
        time.sleep(1)
    
        # --- create a beautiful soup object with the image detail page's html ---
        img_detail_html = browser.html
        imagesoup = BeautifulSoup(img_detail_html, 'html.parser')
    
        # --- create the base url for the fullsize image link ---
        base_url = 'https://astrogeology.usgs.gov'
    
        # --- retrieve the full-res image url and save into a variable ---
        hem_url = imagesoup.find('img', class_="wide-image")['src']
    
        # --- complete the featured image url by adding the base url ---
        img_url = base_url + hem_url

        # --- retrieve the image title using the title class and save into variable ---
        img_title = browser.find_by_css('.title').text
    
        # --- add the key value pairs to python dictionary and append to the list ---
        hemisphere_image_data.append({"title": img_title, "img_url": img_url})
    
        # --- go back to the main page ---
        browser.back()

    # --- Quit the browser after scraping ---
    browser.quit()

    print("Mars Hemisphere Images: Scraping Complete!")
    
    # *****************************************************************************************************************************
    #  Store all values in dictionary
    # *****************************************************************************************************************************

    scraped_data = {
        "news_title": news_title,
        "news_para": news_para,
        "featuredimage_title": featuredimage_title,
        "featuredimage_url": featuredimage_url,
        "latest_tweet": latest_tweet,
        "mars_fact_table": html_table, 
        "hemisphere_images": hemisphere_image_data
    }

    # --- Return results ---
    return scraped_data
