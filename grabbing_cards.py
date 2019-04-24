from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import OrderedDict
import re
import time

def get_deck_from_link(link):

    deck = requests.get(link)
    deck_soup = BeautifulSoup(deck.content, 'html.parser')

    #there are two tabs so without only choosing the paper version you get duplicates which causes more problemsm
    deck_soup_card = deck_soup.find("div", {"id":"tab-paper"})

    card_soup = deck_soup_card.find_all("td", {"class":"deck-col-card"})
    quant_soup = deck_soup_card.find_all("td", {"class":"deck-col-qty"})

    card_quantities = []
    for quant in quant_soup:
        card_quantities.append(int((quant.text).strip()))

    card_names = []
    for card in card_soup:
        card_names.append((card.text).strip())

    deck_list = pd.DataFrame({'cardName': card_names
                                 , 'cardNumber': card_quantities})

    # you have to remove duplicates because there is css in the page for paper and online cards
    # the cards are the same, but the prices are different.  It would have been difficult to implement it in css

    #problem with this logic if the same number of cards are in the sideboard!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    deck_list['count_card'] = deck_list.cardNumber.cumsum()

    # were assuming the deck has 60 cards in it (which most competitive decks do) and the rest are sideboard
    # I should probably add a warning if the full sum is > 75


    deck_list.loc[(deck_list['count_card'] <= 60), 'mainorside'] = 'main'
    deck_list.loc[(deck_list['count_card'] > 60), 'mainorside'] = 'sideboard'

    return deck_list



page = requests.get('https://www.mtggoldfish.com/metagame/standard#paper')

soup = BeautifulSoup(page.content, 'html.parser')
beautifuldata = soup.find_all("span", {"class":"deck-price-paper"})


links_to_search=[]
for span in beautifuldata:
    links = span.findAll(href = re.compile("deck"))

    for a in links:
        #print(a.find_all(href=True))
        #print(a.attrs)
        link = 'http://www.mtggoldfish.com' + a.attrs['href']
        deck_id = a.attrs['href'].rsplit('/',1)[-1].rsplit('#',1)[0]
        #print(deck_id)
        #print(a.text)
        links_to_search.append([link,a.text,deck_id])

all_decks = pd.DataFrame()

links_to_search=links_to_search[0:1]
for data in links_to_search:
    print(data)
    link = data[0]
    name = data[1]
    deck_id = data[2]

    temp_panda = get_deck_from_link(link)

    temp_panda['link'] = link
    temp_panda['name'] = name
    temp_panda['deck_id'] = deck_id
    #print(temp_panda)

    all_decks = pd.concat([all_decks,temp_panda])#all_decks.append(temp_panda)
    time.sleep(5)


print(all_decks)



"""


deck = requests.get('https://www.mtggoldfish.com/deck/1714115#paper')
deck_soup = BeautifulSoup(deck.content, 'html.parser')

#there are two tabs so without only choosing the paper version you get duplicates which causes more problems
deck_soup_card = deck_soup.find("div", {"id":"tab-paper"})

card_soup = deck_soup_card.find_all("td", {"class":"deck-col-card"})
quant_soup = deck_soup_card.find_all("td", {"class":"deck-col-qty"})

card_quantities = []
for quant in quant_soup:
   card_quantities.append(int((quant.text).strip()))

card_names = []
for card in card_soup:
    card_names.append((card.text).strip())

deck_list = pd.DataFrame({'cardName': card_names
                          , 'cardNumber': card_quantities})



#deck_list = deck_list.drop_duplicates()
deck_list['count_card'] = deck_list.cardNumber.cumsum()

#were assuming the deck has 60 cards in it (which most competitive decks do) and the rest are sideboard
#I should probably add a warning if the full sum is > 75
deck_list.loc[(deck_list['count_card']<=60),'mainorside'] = 'main'
deck_list.loc[(deck_list['count_card']>60),'mainorside'] = 'sideboard'


#we are uss
print(deck_list)

"""

"""
card_soup = deck_soup.find_all("td", {"class":["deck-col-qty","deck-col-card"]})

nums = []
card_name = []
card_list=[]
for card in card_soup:
    if nums == '':
        nums = card.text

    else:
        card_name = card.text
        card_list.append([nums,card_name])
        nums=[]
        card_name=[]
    print(card.text)

print(card_list)
"""

    #print(card.find("td",{"class":"deck-col-qty"}))