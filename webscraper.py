import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
import mysql.connector
from datetime import date

#db = mysql.connector.connect(host="127.0.0.1",user="root",passwd="")
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Password"
  #auth_plugin="caching_sha2_password"
)

cur = db.cursor()

def checkTableExists(db, tablename):
    dbcur = db.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

Tname1 = "outbreakTable"

cur.execute('Create database if not exists cdcDB')
cur.execute('use cdcDB')
if checkTableExists(db, Tname1) != True:
    cur.execute('DROP TABLE IF EXISTS `outbreakTable`')
    table ='create table if not exists outbreakTable(id int NOT NULL AUTO_INCREMENT, url varchar(300), headline varchar(200), date varchar(20), details varchar(1000), PRIMARY KEY (id))'
    cur.execute(table)
    cur.execute('ALTER TABLE outbreakTable AUTO_INCREMENT = 1')
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


            #body > div.container.d-flex.flex-wrap.body-wrapper.bg-white > main > div:nth-child(3) > div > div.syndicate > p:nth-child(18)

            #card-header h4 bg-secondary 3-4/6 links working
            checkMainText = newPageContent.find('div', attrs={"class": "card mb-3"})
            #checkMainText1 = newPageContent.select("body > div.container.d-flex.flex-wrap.body-wrapper.bg-white > main > div:nth-child(3) > div > div:nth-child(4) > div > p:nth-child(4)")
            #print checkMainText1
            if checkMainText != None:
                checkMainText = checkMainText.text
                #checkMainText2 = newPageContent.select("body > div.container.d-flex.flex-wrap.body-wrapper.bg-white > main > div:nth-child(3) > div > div.syndicate > div:nth-child(3) > div > div.card.mb-3 > div.card-body.bg-white > p:nth-child(2)")
                #print checkMainText2
            else:
                checkMainText = "unknown"

            urlAtt = url4newpage
            headlineAtt = headline
            dopAtt = dateOfPublication
            main_textAtt = checkMainText


            outbreakObject = {

                "url": url4newpage,
                "headline": headline,
                "date_of_publication": dateOfPublication,
                "main_text": checkMainText ,
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

            cur.execute('insert into outbreakTable (url, headline, date, details) values (%s,%s,%s,%s)',(urlAtt,headlineAtt,dopAtt, main_textAtt))
            cur.execute('select * from outbreakTable')
            #cur.commit()
            rows = cur.fetchall()
            print('Total Row(s):', cur.rowcount)
            for row in rows:
                print(row)

# for i in jsonData:
    # print "URL: "+ i['url']
    # print "HEADLINE: "+ i['headline']
    # print "DATE: " + i['date_of_publication']
    # print "BODY: "+ i['main_text']
    # print "\n"


db.close()
