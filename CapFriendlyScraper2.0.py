#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 23:24:20 2017
version 2.0 of Cap Friendly Scraper 
@author: MattBarlowe
"""
import bs4
import requests
import pandas as pd

#Initializing empty list that will hold the range of years that user wants to scrape
cap_years = []

#this is the code to get the headers of cap table
#that will be appended to the data frames in the write_cap_data function
def get_headers():
    url = 'https://capfriendly.com/browse/active'
    cap_table_headers = []       
    headers = requests.get(url)
    headers_text=bs4.BeautifulSoup(headers.text, "lxml")
    headers_contents = headers_text('th')
    for x in range(len(headers_contents)):
        cap_table_headers.append(headers_contents[x].getText())
    return cap_table_headers
    
#this is the function that will scrape all the data from capfriendly depending on year input
#and return the data in a tuple list
def scrape_data(year):
    #Initializing lists that I will manipulate later and seperate into lists of lists
    cap_table_contents_text = [] 
    images_list = []
    cap_table_contents_slice=[]
    
    #creates variable from funciton input to be manipulated
    cap_year = year
    
    #creates page variable to be incremented so scraper can move through pages of cap data
    page = 1
    
    #creates url string that can be adjusted by year of cap hits requested by function
    #the reason there are two is so the end of url can easily be appended with page number
    #without complex slicing needed
    url = 'https://capfriendly.com/browse/active/' + str(cap_year) + '/caphit/all/all/all/desc/'
    new_url = url
    
    
    
    #loop which moves through pages and scrapes the data on each page for year   
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
        for img in capfriendly_text.find_all('img'):
            if str(img.get('alt')) != "None":       
                images_list.append(img.get('alt'))
            elif str(img.get('src')) == "/images/team/svg/nhl_shield.svg":
                images_list.append("None")
    
        #test to make sure number of team names matches number of players on each page
        print(len(images_list))
        
        #appends the lists initialized above with all data in <td> tags
        for x in range(len(cap_table_contents)):
            cap_table_contents_text.append(cap_table_contents[x].getText())
        
        # this is key to incrementing while loop so loop will eventually end
        page += 1
        new_url = url + str(page)
        
        # these next two lines are test lines to make sure code is working properly
        print(new_url)
        print("WebSite DownLoaded!")
        
        #these two lines slice the contents of cap_table_contents_text into lists
        cap_table_contents_slice = [cap_table_contents_text[i:i + 21] for i in range(0, len(cap_table_contents_text), 21)]
        for x in range(len(images_list)):
            cap_table_contents_slice[x][1] = images_list[x]
    return cap_table_contents_slice


#this function will write the list returned by scrape_data 
#function to a csv file on the desktop
def write_cap_data(cap_list, year):
    cap_data = cap_list
    cap_year = year
    #convert lists to Dataframes and export to CSV
    cap_data_df = pd.DataFrame(cap_data)  
    
    #sets column names from capfriendly table headers 
    cap_data_df.columns = get_headers()            
    
    cap_data_df.to_csv('/Users/MattBarlowe/CapData'+ str(cap_year)+'.csv', index=False, header=True)
    return print('Cap Data saved as /Users/MattBarlowe/CapData'+ str(cap_year)+'.csv')

#function to get year ranges for cap hit scraping 
def get_years():
    years_list = []
    print('Please enter ranges of years you would like to recieve cap hit data. The data starts with 2015 season and ends with 2017.')
    start_year = input("Please enter start year:\n")
    end_year = input("Please enter end year:\n")
    
    #checks to see if year is entered in the right length
    if len(start_year) != 4 or len(end_year) != 4:
        print('Please input year as a 4 digit number. \n')
        return get_years()
    
    #checks to make sure right range of inputs is entered
    if int(start_year) < 2015 or int(end_year) > 2017:
        print('Please input a year within range.\n')
        return get_years()
    
    #checks to see if the range is just one year and returns the a list with only that year in it
    if int(start_year) == int(end_year):
        years_list.append(start_year)
        return years_list
    
    #creates the list holding year range values
    for x in range(int(start_year), (int(end_year) + 1)):
        years_list.append(x)
        
    return years_list
    

cap_years = get_years()
for x in range(len(cap_years)):
    write_cap_data(scrape_data(cap_years[x]), cap_years[x])
    
