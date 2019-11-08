#! /usr/bin/python3

'''
Use requests lib to pull data from URL
Use beautiful soups to parse the data.
Filter the data using an external csv file of keywords
Export the filtered data to a new csv file in column format
'''

from bs4 import BeautifulSoup
import requests # find_all() get_text()
import datetime # needed for timestamp in output.csv

# TODO add print statements to show user the steps
# TODO let user choose which search engine.
# TODO change date stamp in output.csv to keyword stamp. Date stamp at top.

#import keywords from external csv file in a list, replace spaces with + for easy url insertion
file_of_keywords = open("keywords.csv", 'r')
keywords = []
for item in file_of_keywords:
    keywords.append(item.strip().lower().replace(" ","+"))
file_of_keywords.closed

# empty output file to ready it for new data.
with open("output.csv", "w"):
    pass

def get_content(search_term):
    # Use request lib to get homepage content, do your url research
    url = "https://www.bing.com/news/search?q=" +\
        search_term +\
        "&qft=interval%3d%229%22&form=PTFTNR"
    first_request = requests.get(url)
    first_results = first_request.content

    # Use BeautifulSoup to parse the content
    soup1 = BeautifulSoup(first_results, "html5lib")

    # store the useful data in a list, remove the commas for easy csv export
    # Do your html/css research for appropriate tags
    bing_list = []
    for a_tag in soup1(class_='title', href=True):
        bing_list.append(a_tag.text.strip().lower().replace(',',"") + ',')
        bing_list.append(a_tag['href'] + "\n")

    # export data to .csv as well as website name as a header
    #open local file in append mode
    with open("output.csv", "a") as local_file:
        # add stamp to new export data
        local_file.write('\n') # newline ensures column 1
        local_file.write(search_term + '\n')
        # append data to file in column format
        for data in bing_list:
            local_file.write(data) #newline should force column format

print("Searching for terms...")
for each_keyword in keywords:
    get_content(each_keyword)

num_line = sum(1 for line in open("output.csv"))
print("Finished! " + str(num_line) + " lines written to output.csv")
exit(0)
