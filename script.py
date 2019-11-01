#! /usr/bin/python3

'''
Use requests lib to pull data from URL
Use beautiful soups to parse the data.
Filter the data using an external csv file of keywords
Export the filtered data to a new csv file in column format
'''

from bs4 import BeautifulSoup
import requests # find_all() get_text()
import re # regex
import datetime # needed for timestamp in output.csv

# TODO get url as input from user.
# TODO get tag info from user
# TODO perhaps use with all google web site results instead of site specific.
# TODO remove commas from final_headline for better spreadsheet formatting
# TODO get url along with headline.

# Attempt to scrape universityworldnews.com using search bar
# <form> name = "searchbox" <input> class = "input" placeholder = "search" 

# Use request lib to get homepage content
url = "https://www.universityworldnews.com/page.php?page=UW_Main"
first_request = requests.get(url)
coverpage = first_request.content

# Use BeautifulSoup to parse the content
soup1 = BeautifulSoup(coverpage, "html5lib")
coverpage_search = soup1.find_all('a', href=re.compile('^post*'))

# strip the parsed coverpage of all but the inner html (headlines)
stripped_headlines = [article.text.strip().lower() for article in coverpage_search]

#store keywords in a list
file_of_keywords = open("keywords.csv", 'r')
keywords = []
for item in file_of_keywords:
    keywords.append(item.strip().lower())
file_of_keywords.closed

#search stripped_headlines for keywords, 
good_headlines = []
for headline in stripped_headlines:
    for keyword in keywords:
        if keyword in headline:
            # print("success, jeyword in headline " + headline)
            good_headlines.append(headline)

#check good_headlines for duplicates
final_headlines = []
for headline in good_headlines:
    if headline not in final_headlines:
        #remove commas for better csv formatting
        headline = headline.replace(',', '')
        final_headlines.append(headline)

print("length of stripped headlines: " + str(len(stripped_headlines)))
print("length of good headlines: " + str(len(good_headlines)))
print("length of final headlines: " + str(len(final_headlines)))

# export final_headlines to .csv as well as website name as a header
#open local file in append mode
with open("output.csv", "a") as local_file:
    # add stamp to new export data
    local_file.write('\n') # newline ensures column 1
    todays_date = str(datetime.datetime.now().date())
    local_file.write(str(todays_date) + "," + '\n') 
    local_file.write(str(url) + ",")
    # append data to file in column format
    for headline in final_headlines:
        local_file.write(headline + '\n') #newline should force column format
        local_file.write(",")
    

exit(0)
