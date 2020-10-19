from bs4 import BeautifulSoup # Installed package beautifulsoup4 in Django environment
import requests # Installed package requests in Django environment

import time
start_time = time.time()

# Built with assistance from Benny Lin (thank you very much!)
# Look into web sockets for real-time refreshing (or something like it)
# Database instructor Chris Bautista uses for his eSports projects: Neo4J

main_link = 'https://feheroes.gamepedia.com'
# gets data
r = requests.get('https://feheroes.gamepedia.com/List_of_Heroes')


soup = BeautifulSoup(r.content, "html.parser") # converts to html

# print(soup) # Prints *ALL* the HTML on that page
# print(soup.find( "h1" , {"class": "firstHeading"})) # Finds first instance of h1 tag with the class firstHeading - includes the HTML

# header = soup.find( "h1" , {"class": "firstHeading"})
# print(header.get_text()) # Gets the text between the tags


table = soup.find("table", {"class": "sortable"}) # Note: figure out how to search with multiple classes

list_of_heroes = table.find_all("tr", {"class": "hero-filter-element"})

url_list = []
for k in range(len(list_of_heroes)):
    cur_hero = list_of_heroes[k] # Current hero
    link = cur_hero.find("a")
    href_link = link['href']
    print("Name of hero =",href_link[1::])
    page_link = main_link + href_link
    url_list.append(page_link)

print("Number of heroes =",str(len(list_of_heroes)))
url_Alm_SK = url_list[7]

r = requests.get(url_Alm_SK) # Get all the HTML
soup = BeautifulSoup(r.content, "html.parser") # converts to html
all_tables = soup.find_all("table", {"class": "wikitable default"})
level_1_table = all_tables[0]
all_trs =level_1_table.find_all("tr")
last_tr = all_trs[-1] # Gets last row: 5* rarity stats
all_tds = last_tr.find_all("td")
stats = []
for k in range(1,len(all_tds)-1):
    print(all_tds[k].get_text())
# level_40_table = all_tables[1]

num_seconds = time.time() - start_time
print(f"Run time = {num_seconds} seconds") 