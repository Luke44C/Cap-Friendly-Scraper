# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 23:58:49 2018

@author: Luke4
"""
import bs4
import requests
import pandas as pd

#Initializing empty list that will hold the range of years that user wants to scrape
cap_years = []

url = 'https://capfriendly.com/browse/active'
cap_table_headers = []       
    
#opens CapFriendly and pulls the text from the Table Header tag
headers = requests.get(url)
headers_text=bs4.BeautifulSoup(headers.text, "lxml")
headers_contents = headers_text('th')
for x in range(len(headers_contents)):
    #if headers_contents[x].getText() != '' and not headers_contents[x].getText().isspace():
    cap_table_headers.append(headers_contents[x].getText().encode('utf-8'))
    
cap_table_contents_text = [] 
images_list = []
cap_table_contents_slice=[]

#creates variable from funciton input to be manipulated
cap_year = 2017

#creates page variable to be incremented so scraper can move through pages of cap data
page = 1

#creates url string that can be adjusted by year of cap hits requested by function
#the reason there are two is so the end of url can easily be appended with page number
#without complex slicing needed
url = 'https://capfriendly.com/browse/active/' + str(cap_year) + '/caphit/all/all/all/desc/'
new_url = url

while not new_url.endswith('20'):  
    #Creates a response object to test to see if end of cap data has happened
    status_test = requests.get(new_url)
    status_test.raise_for_status()
    
    #initial pull of html data from CapFriendly site
    capfriendly = requests.get(new_url)
    
    #These next 3 lines of code breaks down the site with BS4
    capfriendly_text =bs4.BeautifulSoup(capfriendly.text, "lxml") 
    
    #breaks down the html into just the contents of the <td> tags
    cap_table_contents=capfriendly_text('td')  
    
    #checks to see if next iteration of URL contains any data in tables and 
    #if table is empty breaks the loop
    if not cap_table_contents:
        break
        
    #breaks down the images into actual team names and provides none if the player
    #no longer plays on an NHL team 
#    for img in capfriendly_text.find_all('img'):
#        if img.get('alt').encode('utf-8') != "None":       
#            images_list.append(img.get('alt'))
#        elif img.get('src').enconde('utf-8') == "/images/team/svg/nhl_shield.svg":
#            images_list.append("None")

    #test to make sure number of team names matches number of players on each page
    print(len(images_list))

    #appends the lists initialized above with all data in <td> tags
    for x in range(len(cap_table_contents)):
        cap_table_contents_text.append(cap_table_contents[x].getText().encode('utf-8'))
    
    # this is key to incrementing while loop so loop will eventually end
    page += 1
    new_url = url + str(page)
    
    # these next two lines are test lines to make sure code is working properly
    print(new_url)
    print("WebSite DownLoaded!")
    
    #these two lines slice the contents of cap_table_contents_text into lists
    cap_table_contents_slice = [cap_table_contents_text[i:i + 22] for i in range(0, len(cap_table_contents_text), 22)]

        
    #deleting the empty elements of the lists
    #for x in cap_table_contents_slice:
    #    del x[18]
    #    del x[6]
        
cap_data_df = pd.DataFrame(cap_table_contents_slice)

cap_data_df.columns = cap_table_headers

cap_data_df.to_csv('C:\Users\Luke4\projects\Cap-Friendly-Scraper\salaryData.csv', index=False, header=True)
