import requests
import json
import time
import urllib.parse
import csv

from bs4 import BeautifulSoup

import random

from itertools import cycle

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

from lxml.html import fromstring
user_agent = random.choice(user_agent_list)
#Set the headers
headers = {'User-Agent': user_agent}


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table=soup.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    proxies = []
    for row in rows:
        cols=row.find('td')
        for item in row:
            try:
                #print(int(item.text))
                cols = str(cols.text)+":"+str(int(item.text))
                proxies.append(cols)
            except:
                pass

    return proxies





def amazon_price(query):

    url = "https://www.amazon.com/s?k="
    url += urllib.parse.quote_plus(query)
    return url


def book_check(query):
    url = "https://www.amazon.com/s?k="
    url += urllib.parse.quote_plus(query)
    proxies = get_proxies()
    #print(proxies)
    proxy_pool = cycle(proxies)
    for i in range(1, 11):
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        print("Request #%d" % i)
        try:
            resp = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            rows=soup.find_all("span", class_='a-offscreen')
            otherrows=soup.find_all('span')
            moredivs=soup.find_all('div')
            print(moredivs)
            #print(soup)
            print("**************************************************")
            print(rows)
            print(otherrows)
            break
        except:
            print("Skipping. Connnection error")




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
            print(book_check(product))
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