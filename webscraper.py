import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
from datetime import date

def fetchNewPages(url):
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
    if urls != None:
        url4newpage = urls.get('href')
        if pattern.match(url4newpage):
            newPageContent = fetchNewPages(url4newpage)

            ans1 = newPageContent.find("h1", attrs={"id": "content"})
            if ans1 is None:
                print Unknown
                continue
            else:
                ans1 = newPageContent.find("h1", attrs={"id": "content"}).text.encode('utf-8')
            ans = newPageContent.find("p").text.encode('utf-8')
            match = re.search(r'\s \d{2}, \d{4}', ans)
            ans = re.sub('[pP]osted ','', ans)
            pattern1 = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
            match1 = re.search(pattern1, ans)
            if match1 is None:
                continue
            s1 = match1.group(0)
            d = datetime.datetime.strptime(s1, '%B %d, %Y')
            paragraph_text = newPageContent.find("p")
            print url4newpage
            print (d.strftime('%Y-%m-%d'))
            print ans1
            print "\n"

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

#for i in jsonData:
    #print i['url']
    #print i['title']
    #print i['date_of_publication']
    #print i['headline']
    #print "\n"
