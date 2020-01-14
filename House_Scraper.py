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

# Gets the property info on the given page
def getPropertyInfo(pageNum):
    url = 'https://www.domain.com.au/sale/wetherill-park-nsw-2164/?excludeunderoffer=1&page=' + str(pageNum)
    response  = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    houses = soup.findAll("li", {"class": "css-1b4kfhp"})

    for house in houses:
        price = house.find('p', {'class': 'listing-result__price'})
        location = house.find('span', {'class': 'address-line1'})
        property_type = house.find('div', {'class': 'listing-result__property-type'})
        link = house.find_all('a')

        if price == None or location ==  None or property_type == None or (price.text)[0] != '$':
            continue
        else:
            prices.append(price.text)
            newLocation = (location.text).replace(',\xa0', '')
            locations.append(newLocation)
            property_types.append(property_type.text)
            links.append(link)


prices = []
locations = []
property_types = []
links = []

for i in range(1, 20):
    getPropertyInfo(i)

print(property_types)
#print(prices) 
#print(locations)




# Methods
def fixPrice(price):

    if price[0] == '$':
        newPrice = ((price.replace('$', '')).replace(',', '')).replace(' ', '')


    return int(newPrice)

# Testing
def test_one():

    assert fixPrice('$665,000 ') == 665000
    assert fixPrice()