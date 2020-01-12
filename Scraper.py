### IMPORTS
from bs4 import BeautifulSoup
import requests
import time
import smtplib
import email

#############################
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
Continue = True


def check_price_amazon():
    response = requests.get(url, headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')



def check_price_ebay():
    response = requests.get(url, headers=headers)

    # If the response is ok, scrape the page
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id="itemTitle").get_text()
        title = title[16:]
        price = soup.find(id="prcIsum").get_text()
        price = price.replace(',', '')
        converted_price = float(price[4:])

        print(f"Tracking item: {title}")
        print(f"Current price: {converted_price}")


    if (converted_price <= desiredPrice):
        send_mail(sendTo, desiredPrice, title)


def send_mail(given_email, price, itemName):
    msg = email.message_from_string(f"Price of your {itemName} just went down to ${price}!\n\n Checkout your link at {url}")
    
    base = 'BozinovskiDaniel@hotmail.com'
    
    msg['From'] = base
    msg['To'] = given_email
    msg['Subject'] = f"Price of Your Item Just Went Down To ${price}"

    s = smtplib.SMTP("smtp.live.com", 587)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(base, 'nba302311')

    s.sendmail(base, given_email, msg.as_string())

    s.quit()
    global Continue
    Continue = False
    print('Price has been lowered')

# Email, Link, Desired Price

website = input("Amazon (A) / Ebay (E) ? ")
while website != 'A' and website != 'E':
    website = input("Please type 'A' for Amazon or 'E' for Ebay: ")

url = input("Enter the Url of the Item: ")
sendTo = input("Enter your E-mail: ")
desiredPrice = float(input("Enter Desired Price: "))
print("########## CHECKING PRICE ##########")


while Continue:
    if website == 'A':
        check_price_amazon()
    elif website == 'E':
        check_price_ebay()
    else:
        print('Error')

    time.sleep(10) # Intervals to scrape the websites
