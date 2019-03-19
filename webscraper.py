import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://www.cdc.gov/outbreaks/'

response = requests.get(url)

content = BeautifulSoup(response.content, "html.parser")

OutbreakArr = []
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

with open('data.json') as json_data:
    jsonData = json.load(json_data)

for i in jsonData:
    print i['url']
    print i['date_of_publication']
    print i['headline']
