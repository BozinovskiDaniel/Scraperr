### Imports ###
from bs4 import BeautifulSoup
import re
import requests
from pandas import DataFrame
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import numpy
################

sns.set()
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

########## FUNCTIONS ##########
def convert_price(price):
    
    if '-' in price:
        array = price.split('-')
        newPrice = ((array[0].replace(',', '')).replace('$', '')).replace('.', '')
    else:
        array = price.split(' ')
        newPrice = ((array[0].replace(',', '')).replace('$', '')).replace('.', '')

    return int(newPrice)

def test_one():
    assert convert_price('$738,000 negotiable ') == 738000

def test_two():
    assert convert_price('$650,000 - CONTACT AGENT ') == 650000

def test_three():
    assert convert_price('$693,690 Walking to future Business Park ') == 693690


# Gets the property info on the given page
def getPropertyInfo(pageNum):

    # https://www.domain.com.au/sale/wetherill-park-nsw-2164/?excludeunderoffer=1&page=
    # https://www.domain.com.au/sale/west-wollongong-nsw-2500/?excludeunderoffer=1&page=
    # https://www.domain.com.au/sale/kellyville-nsw-2155/?excludeunderoffer=1&page=
    # https://www.domain.com.au/sale/jervis-bay-nsw-2540/?excludeunderoffer=1&page=
    # https://www.domain.com.au/sale/marsden-park-nsw-2765/?keywords=nsw&sort=price-asc&page=
    # https://www.domain.com.au/sale/?excludeunderoffer=1&page=

    url = 'https://www.domain.com.au/sale/schofields-nsw-2762/?excludeunderoffer=1&page=' + str(pageNum)
    response  = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    houses = soup.findAll("li", {"class": "css-1b4kfhp"})

    for house in houses:
        price = house.find('p', {'class': 'listing-result__price'})
        location = house.find('span', {'class': 'address-line1'})
        suburb = house.find('span', {'class': 'address-line2'})
        property_type = house.find('div', {'class': 'listing-result__property-type'})
        link = house.find_all('a')


        if price == None or location ==  None or property_type == None or (price.text)[0] != '$':
            continue
        elif ('m' in (price.text)) or ('k' in (price.text)) or ('M' in (price.text)) or ('K' in (price.text)):
            continue
        else:
            prices.append(convert_price(price.text))
            newLocation = (location.text).replace(',\xa0', '')
            locations.append(newLocation)
            property_types.append(property_type.text)
            urls.append(link[0].get('href'))
            suburbs.append((suburb.text).replace(' ', ', '))

###############################


prices = []
suburbs = []
locations = []
property_types = []
urls = []

print('########## Fetching Data ##########')

for i in range(1, 150):
    getPropertyInfo(i)


properties = {'Type': property_types,
              'Suburb': suburbs,
              'Location': locations, 
              'Price': prices,
              'URL': urls
              }

df = DataFrame(properties, columns = ['Type', 'Suburb', 'Location', 'Price', 'URL'])

print('########## Exporting Data ##########')

export_excel = df.to_excel (r'C:\Users\bozin\Desktop\Schofields.xlsx', index = None, header=True)

print('########## COMPLETE!!! ##########')
