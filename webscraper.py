import requests
from bs4 import BeautifulSoup
import json
import re



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

            #checks if the link is none
            ans = newPageContent.find("h1", attrs={"id": "content"})
            print ans

            if ans != None:
                headline = newPageContent.find("h1", attrs={"id": "content"}).text.encode('utf-8')
            else:
                headline = "unknown"

            outbreakObject = {

                "url": url4newpage,
                "headline": headline,
                #"date_of_publication": outbreaks.find('span', attrs={"class": "item-pubdate"}).text.encode('utf-8'),
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
    #print i['date_of_publication']
    #print i['headline']
    print "\n"
