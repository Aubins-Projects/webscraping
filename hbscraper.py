import requests
import json
import time
from bs4 import BeautifulSoup

url = "https://www.humblebundle.com/"




resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')

bundles = soup.find('script', type='application/json').text



data = json.loads(bundles)


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

            # Add one product tier to our datastructure
            tier_dict[tiername] = {"products": product_names}

    # After we build our datastructure...
    for tiername, tierinfo in tier_dict.items():
        print(tiername)
        print("########################")
        print("\n".join(tierinfo['products']))
    print("\n\n")