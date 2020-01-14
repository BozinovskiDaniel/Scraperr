### Imports
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
################

sns.set()
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

# Properties = {'type': [], 'location': [], 'price': []}

# Gets the property info on the given page
def getPropertyInfo(pageNum):

    url = 'https://www.domain.com.au/sale/wetherill-park-nsw-2164/?excludeunderoffer=1&page=' + str(pageNum)
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
        else:
            prices.append(price.text)
            newLocation = (location.text).replace(',\xa0', '')
            locations.append(newLocation)
            property_types.append(property_type.text)
            links.append(link)
            suburbs.append((suburb.text).replace(' ', ', '))


prices = []
suburbs = []
locations = []
property_types = []
links = []

print('########## Fetching Data ##########')

for i in range(1, 40):
    getPropertyInfo(i)


properties = {'Type': property_types,
              'Suburb': suburbs,
              'Location': locations, 
              'Price': prices
              }

df = DataFrame(properties, columns = ['Type', 'Suburb', 'Location', 'Price'])

print('########## Exporting Data ##########')
export_excel = df.to_excel (r'C:\Users\bozin\Desktop\HouseData.xlsx', index = None, header=True)

print('########## COMPLETE!!! ##########')