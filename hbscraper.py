import requests
import json
import time
import urllib.parse
import csv

from bs4 import BeautifulSoup




def amazon_price(query):

    url = "https://www.amazon.com/s?k="
    url += urllib.parse.quote_plus(query)
    return url


def book_check(query):
    new_url="https://www.booksprice.com/compare.do?inputData="
    new_url += urllib.parse.quote_plus(query)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for link in soup.find_all('a'):
        if(len(link.get('href'))==10):
#            print(link)
            value=link.get('href')
            break
#    print(value)
    new_url="https://www.booksprice.com/comparePrice.do?l=y&searchType=compare&inputData="
    new_url +=value
    new_url += "&dontShowRentals=true&fromPrice=true"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    time.sleep(5)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')


url = "https://www.humblebundle.com/"




resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')

bundles = soup.find('script', type='application/json').text



data = json.loads(bundles)

csv_dict={}

list_of_urls=[]
list_of_bundles=[]
for item in data['navbar']['productTiles']:

    url_edit = "https://www.humblebundle.com"
    parsed_data1 = item['human_name']
    parsed_data = item['product_url']
    if parsed_data.find('/books/') != -1:
        url_edit+=parsed_data

        list_of_urls.append(url_edit)
        list_of_bundles.append(parsed_data1)



counter=0
product_dict = {}

for url in list_of_urls:
    tier_dict = {}
    time.sleep(.5)
    resp=requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for div in soup.find_all("span", {'class': 'sr-only'}):
        div.decompose()
    tiers = soup.select(".dd-game-row")
    multi=len(list_of_bundles[counter])+2
    print("@"*multi)
    print("BUNDLE NAME: ", list_of_bundles[counter])
    print("@"*multi)
    counter+=1
    for tier in tiers:
        # Only for sections that have a headline
        if tier.select(".dd-header-headline"):
            # Grab tier name (and price)
            tiername = tier.select(".dd-header-headline")[0].text.strip()

            # Grab tier product names
            product_names = tier.select(".dd-image-box-caption")
            product_names = [prodname.text.strip() for prodname in product_names]
            for product in product_names:
                #print(amazon_price(product))
                product_dict[product]={
                    "link": amazon_price(product),
                    "price": "unknown"
                                       }

            tier_dict[tiername] = {"products": product_names}

    for tiername, tierinfo in tier_dict.items():

        print(tiername)
        print("########################")
        #print("\n".join(tierinfo['products']))
        for product in tierinfo['products']:
            print(product)
            print(product_dict[product])
            csv_dict[product] = {
                "Book": product,
                "Bundle":list_of_bundles[counter-1] ,
                "Amazon Link":product_dict[product]['link'],
                "Tier": tiername
            }
    print("\n\n")


#print(csv_dict)
csv_file = "books.csv"
csv_columns=['Book', 'Bundle', 'Amazon Link', 'Tier']

try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in csv_dict:
            #print(data)
            #print(csv_dict[data])
            writer.writerow(csv_dict[data])

except IOError:
    print("I/O error")