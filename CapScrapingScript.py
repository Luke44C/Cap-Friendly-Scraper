# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a scraper designed to scrape the 2017 NHL cap hits.
Adding some more comments in here to practice using Github branches and merging
"""
import bs4, requests
import pandas as pd
url = 'https://capfriendly.com/browse/active/2017/caphit/all/all/all/desc/'
new_url = url
page = 1
cap_table_headers = []       #this is the code to get the headers of cap table
headers = requests.get(url)
headers_text=bs4.BeautifulSoup(headers.text, "lxml")
headers_contents = headers_text('th')
for x in range(len(headers_contents)):
    cap_table_headers.append(headers_contents[x].getText())

print(cap_table_headers)
    
cap_table_contents_text = [] #Initializing lists that I will manipulate later to sperate into tuples
images_list = []             #this list will contain the team name as capfriendly lists teams by img


while not new_url.endswith('16'):  #this is the code to scrape the contents of Capfriendly tables
    capfriendly = requests.get(new_url)
    capfriendly_text =bs4.BeautifulSoup(capfriendly.text, "lxml") #These 3 lines of code breaks down the site with BS4
    cap_table_contents=capfriendly_text('td')  #breaks down the html into just the contents of the <td> tags
    for img in capfriendly_text.find_all('img'):#breaks down the images into actual team names and provides none if thpe player
        if str(img.get('alt')) != "None":       #no longer plays on an NHL team 
            images_list.append(img.get('alt'))
        elif str(img.get('src')) == "/images/team/svg/nhl_shield.svg":
                images_list.append("None")
    print(len(images_list)) #test to make sure number of team names matches number of players on each page
    for x in range(len(cap_table_contents)):
        cap_table_contents_text.append(cap_table_contents[x].getText())#appends the lists initialized above with all data in <td> tags
    page += 1
    new_url = url + str(page)# this is key to incrementing while loop so loop will eventuall end
    print(new_url)# these next two lines are test lines to make sure code is working properly
    print("WebSite DownLoaded!")
    
#Code below slices cap content into lists inside main list that corresponds the stats to each player in a row
cap_table_contents_slice = [cap_table_contents_text[i:i + 21] for i in range(0, len(cap_table_contents_text), 21)]
for x in range(len(images_list)):
    cap_table_contents_slice[x][1] = images_list[x]
    
cap_table_plus_headers = cap_table_headers + cap_table_contents_slice


cap_df = pd.DataFrame(cap_table_contents_slice)  #convert lists to Dataframes and export to CSV
cap_df.columns = cap_table_headers               #sets column names from capfriendly table headers 
cap_df.to_csv('/Users/MattBarlowe/CapData.csv', index=False, header=True)
