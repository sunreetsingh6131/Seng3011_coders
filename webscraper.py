import requests
from bs4 import BeautifulSoup
import json
import re


def fetchNewPages(url):
    #url = 'https://www.cdc.gov/outbreaks/'
    response = requests.get(url)
    content = BeautifulSoup(response.content, "html.parser")
    return content;

content = fetchNewPages('https://www.cdc.gov/outbreaks/')

OutbreakArr = []
usBasedBox = content.find('div', attrs={"class": "card-body bg-tertiary"})
bulletPoints = usBasedBox.find('ul', attrs={"class": "list-bullet feed-item-list"})

pattern = re.compile("^https")


for outbreaks in bulletPoints.findAll('li'):
    urls = outbreaks.find('a')

    if urls != None: #and "https" in urls:
        url4newpage = urls.get('href')
        if pattern.match(url4newpage):
            #print url4newpage
            newPageContent = fetchNewPages(url4newpage)
            newPageContentTitle = newPageContent.find("button", attrs={"id": "sectionNavButton"})
            print newPageContentTitle

            ans = newPageContentTitle.find("span", attrs={"class": "mobile-title"}).text.encode('utf-8')
            print ans
            outbreakObject = {

                "url": url4newpage,
                #url1 = outbreaks['href'],
                #url1 = outbreaks.find("a").get("href"),
                #"url": url,
                #"title": newPageContentTitle.find("span", attrs={"class": "mobile-title"}).text.encode('utf-8'),
                #"date_of_publication": outbreaks.find('span', attrs={"class": "item-pubdate"}).text.encode('utf-8'),
                #"headline": outbreaks.find('a', attrs={"class": "feed-item-title"}).text.encode('utf-8'),
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
    #print i['title']
    #print i['date_of_publication']
    #print i['headline']
    print "\n"
