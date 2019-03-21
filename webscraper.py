import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
from datetime import date


# class Student(object):
#     name = ""
#     age = 0
#     major = ""
#
# def make_student(name, age, major):
#     student = Student()
#     student.name = name
#     student.age = age
#     student.major = major
#     # Note: I didn't need to create a variable in the class definition before doing this.
#     student.gpa = float(4.0)
#     return student

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
            #checks if the link is none
            checkHeadline = newPageContent.find("h1", attrs={"id": "content"})
            if checkHeadline != None:
                headline = newPageContent.find("h1", attrs={"id": "content"}).text.encode('utf-8')
            else:
                headline = "unknown"

            checkTime = newPageContent.find("p").text.encode('utf-8')
            #print checkTime

            match = re.search(r'\s \d{2}, \d{4}', checkTime)
            #print match
            checkTime = re.sub('[pP]osted ','', checkTime)
            #print checkTime
            pattern4time = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
            matchTime = re.search(pattern4time, checkTime)
            #print matchTime
            if matchTime is None:
                except1 = newPageContent.find('span', attrs={"class": "text-red"}) #.find("span", attrs={"class": "text-red"})
                if except1 != None:
                    pattern4time = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
                    matchTime = re.search(pattern4time, except1.text)
                    s1 = matchTime.group(0)
                    d = datetime.datetime.strptime(s1, '%B %d, %Y')
                    paragraph_text = newPageContent.find("p")
                    dateOfPublication = d.strftime('%Y-%m-%d')
                else:
                    dateOfPublication = "unknown"
            else:
                s1 = matchTime.group(0)
                #print s1
                d = datetime.datetime.strptime(s1, '%B %d, %Y')
                paragraph_text = newPageContent.find("p")
                dateOfPublication = d.strftime('%Y-%m-%d')

            outbreakObject = {

                "url": url4newpage,
                "headline": headline,
                "date_of_publication": dateOfPublication,
                #"headline": outbreaks.find('a', attrs={"class": "feed-item-title"}).text.encode('utf-8'),
                #"main_text": tweet.find('p', attrs={"class": "likes"}).text.encode('utf-8'),
                #"reports": tweet.find('p', attrs={"class": "shares"}).text.encode('utf-8')

                # {"reports": [
                #     {   "diseases": 100,
                #         "syndrome": "reception",
                #         "reported_events": 50,
                #         "comments": 75
                #     },
                # ]},
            }
            OutbreakArr.append(outbreakObject)
            with open('data.json', 'w') as outfile:
                json.dump(OutbreakArr, outfile)

            with open('data.json') as json_data:
                jsonData = json.load(json_data)


for i in jsonData:
    print i['url']
    print i['headline']
    print i['date_of_publication']
    #print i['headline']
    print "\n"
