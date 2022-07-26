# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)



# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# #Retrieve each item that contains a img
results = img_soup.find("div", class_ = 'collapsible results')
mars_img = results.find_all('div', class_='item')

#Get the image link
links = browser.find_by_css('a.product-item img')

for i in range(len(links)):
    #Create empty dictionary
    hemispheres = {}
    
    #Get the image link
    browser.find_by_css('a.product-item img')[i].click()

    #Scrape the title
    mars_title = browser.find_by_css("h2.title").text

    # find the relative image url
    sample = browser.links.find_by_text('Sample').first
    img_url_rel = sample['href']

    # # Use the base url to create an absolute url
    # image_urls = f'https://marshemispheres.com/{img_url_rel}'
    
    #Add to dictionary
    hemispheres["img_url"] = img_url_rel
    hemispheres["title"] = mars_title
    
    #Add to list
    hemisphere_image_urls.append(hemispheres)

    #Go back a page to start scrape again
    browser.back()

# print(hemisphere_image_urls)

# OPTIONAL CODE
# # 3. Write code to retrieve the image urls and titles for each hemisphere.
# for i in range(4):
#     #create empty dictionary
#     hemispheres = {}
#     browser.find_by_css('a.product-item img')[i].click()
#     element = browser.find_link_by_text('Sample').first
#     img_url = element['href']
#     title = browser.find_by_css("h2.title").text
#     hemispheres["img_url"] = img_url
#     hemispheres["title"] = title
#     hemisphere_image_urls.append(hemispheres)
#     browser.back()



# 5. Quit the browser
browser.quit()