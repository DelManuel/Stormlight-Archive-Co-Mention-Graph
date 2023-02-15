#%%
from bs4 import BeautifulSoup as bs
import requests
import pickle
#%% To scrap the coppermind to get the list of characters 
coppermind_url = "https://coppermind.net/wiki/Category:Stormlight_Archive"
coppermind_page = requests.get(coppermind_url)

soup = bs(coppermind_page.content, 'html.parser')
category_pages = soup.find_all(class_="mw-category-group")

#%% We go through each category to save the coppermind pages
important_pages = []

for letter_subsection in category_pages[24:48]:
    letter_subsection = str(letter_subsection)
    for i, character in enumerate(letter_subsection):
        counter = 0
        # We look for wiki pages
        if character == "w" and letter_subsection[i:i+5] == "wiki/": 
            # We obtain the name of the page
            while letter_subsection[i+5+counter] != '"':
                counter += 1
                
            name = letter_subsection[i+5:i+5+counter]
            important_pages.append(name)

# %% We go through the pages and check that the important pages are characters
character_list = []

for page in important_pages:

    url = requests.get("https://coppermind.net/wiki/"+page)
    soup = bs(url.content, 'html.parser')
    # We get the table from the page that contains information about the type of page,
    # whether it´s a location, a group of people or a character.
    table = soup.find_all('table',class_="infobox side", id = "Character")
    
    if table != []: # If it could find the table for the character, we save the page.
        character_list.append(page)

#%% To save the character list 
pickle.dump(character_list, open(f'character_list.pickle', 'wb'))
