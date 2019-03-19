import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import re

url = 'https://www.cdc.gov/outbreaks/'
print(hi)
response = requests.get(url)

content = BeautifulSoup(response.content, "html.parser")

OutbreakArr = []
print(content)
for outbreaks in content.findAll('div', attrs={"class": "card-body bg-tertiary"}):
    outbreakObject = {
        "url": url,
        "date_of_publication": outbreaks.find('span', attrs={"class": "item-pubdate"}).text.encode('utf-8'),
        "headline": outbreaks.find('a', attrs={"class": "feed-item-title"}).text.encode('utf-8'),
        #"main_text": tweet.find('p', attrs={"class": "likes"}).text.encode('utf-8'),
        #"reports": tweet.find('p', attrs={"class": "shares"}).text.encode('utf-8')
    }
    OutbreakArr.append(outbreakObject)
with open('data.json', 'w') as outfile:
    json.dump(OutbreakArr, outfile)
