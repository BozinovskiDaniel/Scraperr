### Imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
################

sns.set()
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

url = 'https://www.domain.com.au/sale/wetherill-park-nsw-2164/?excludeunderoffer=1'

response  = requests.get(url, headers=headers)

if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')

    houses = soup.findAll("li", {"class": "css-1b4kfhp"})
    prices = []
    locations = []


    for i in range(0, 20):
        price = houses[i].find('p', {'class': 'listing-result__price'})
        location = houses[i].find('span', {'class': 'address-line1'})


        if price == None or location ==  None:
            continue
        else:
            prices.append(price.text)
            newLocation = (location.text).replace(',\xa0', '')
            locations.append(newLocation)

    print(locations)
    print(prices)
    


