# import requests
# from bs4 import BeautifulSoup
# import json
# import re
# import datetime
# import mysql.connector
# from datetime import date
#
# #db = mysql.connector.connect(host="127.0.0.1",user="root",passwd="")
# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="Password"
#   #auth_plugin="caching_sha2_password"
# )
#
# cur = db.cursor()
#
# def checkTableExists(db, tablename):
#     dbcur = db.cursor()
#     dbcur.execute("""
#         SELECT COUNT(*)
#         FROM information_schema.tables
#         WHERE table_name = '{0}'
#         """.format(tablename.replace('\'', '\'\'')))
#     if dbcur.fetchone()[0] == 1:
#         dbcur.close()
#         return True
#
#     dbcur.close()
#     return False
#
# Tname1 = "outbreakTable"
#
# cur.execute('Create database if not exists cdcDB')
# cur.execute('use cdcDB')
# if checkTableExists(db, Tname1) != True:
#     #cur.execute('DROP TABLE IF EXISTS `outbreakTable`')
#     table ='create table if not exists outbreakTable(id int NOT NULL AUTO_INCREMENT, url varchar(300), headline varchar(200), date varchar(20), details varchar(1000), PRIMARY KEY (id))'
#     cur.execute(table)
#     cur.execute('ALTER TABLE outbreakTable AUTO_INCREMENT = 1')
# else:
#     cur.execute('DROP TABLE IF EXISTS `outbreakTable`')
#     table ='create table if not exists outbreakTable(id int NOT NULL AUTO_INCREMENT, url varchar(300), headline varchar(200), date varchar(20), details varchar(1000), PRIMARY KEY (id))'
#     cur.execute(table)
#     cur.execute('ALTER TABLE outbreakTable AUTO_INCREMENT = 1')
# # class Student(object):
# #     name = ""
# #     age = 0
# #     major = ""
# #
# # def make_student(name, age, major):
# #     student = Student()
# #     student.name = name
# #     student.age = age
# #     student.major = major
# #     # Note: I didn't need to create a variable in the class definition before doing this.
# #     student.gpa = float(4.0)
# #     return student
#
# def fetchNewPages(url):
#     response = requests.get(url)
#     content = BeautifulSoup(response.content, "html.parser")
#     return content;
#
# content = fetchNewPages('https://www.cdc.gov/outbreaks/')
#
# OutbreakArr = []
# usBasedBox = content.find('div', attrs={"class": "card-body bg-tertiary"})
# bulletPoints = usBasedBox.find('ul', attrs={"class": "list-bullet feed-item-list"})
#
# pattern = re.compile("^https")
#
# for outbreaks in bulletPoints.findAll('li'):
#     urls = outbreaks.find('a')
#     if urls != None:
#         url4newpage = urls.get('href')
#
#         if pattern.match(url4newpage):
#             newPageContent = fetchNewPages(url4newpage)
#
#             #checks if the link is none
#             checkHeadline = newPageContent.find("h1", attrs={"id": "content"})
#             if checkHeadline != None:
#                 headline = newPageContent.find("h1", attrs={"id": "content"}).text.encode('utf-8')
#             else:
#                 headline = "unknown"
#
#             checkTime = newPageContent.find("p").text.encode('utf-8')
#             #print checkTime
#
#             match = re.search(r'\s \d{2}, \d{4}', checkTime)
#             #print match
#             checkTime = re.sub('[pP]osted ','', checkTime)
#             #print checkTime
#             pattern4time = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
#             matchTime = re.search(pattern4time, checkTime)
#             #print matchTime
#             if matchTime is None:
#                 except1 = newPageContent.find('span', attrs={"class": "text-red"}) #.find("span", attrs={"class": "text-red"})
#                 if except1 != None:
#                     pattern4time = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
#                     matchTime = re.search(pattern4time, except1.text)
#                     s1 = matchTime.group(0)
#                     d = datetime.datetime.strptime(s1, '%B %d, %Y')
#                     paragraph_text = newPageContent.find("p")
#                     dateOfPublication = d.strftime('%Y-%m-%d')
#                 else:
#                     dateOfPublication = "unknown"
#             else:
#                 s1 = matchTime.group(0)
#                 #print s1
#                 d = datetime.datetime.strptime(s1, '%B %d, %Y')
#                 paragraph_text = newPageContent.find("p")
#                 dateOfPublication = d.strftime('%Y-%m-%d')
#
#
#             #body > div.container.d-flex.flex-wrap.body-wrapper.bg-white > main > div:nth-child(3) > div > div.syndicate > p:nth-child(18)
#
#             #card-header h4 bg-secondary 3-4/6 links working
#             checkMainText = newPageContent.find('div', attrs={"class": "card mb-3"})
#             #checkMainText1 = newPageContent.select("body > div.container.d-flex.flex-wrap.body-wrapper.bg-white > main > div:nth-child(3) > div > div:nth-child(4) > div > p:nth-child(4)")
#             #print checkMainText1
#             if checkMainText != None:
#                 checkMainText = checkMainText.text
#                 #checkMainText2 = newPageContent.select("body > div.container.d-flex.flex-wrap.body-wrapper.bg-white > main > div:nth-child(3) > div > div.syndicate > div:nth-child(3) > div > div.card.mb-3 > div.card-body.bg-white > p:nth-child(2)")
#                 #print checkMainText2
#             else:
#                 checkMainText = "unknown"
#
#             urlAtt = url4newpage
#             headlineAtt = headline
#             dopAtt = dateOfPublication
#             main_textAtt = checkMainText
#
#
#             outbreakObject = {
#
#                 "url": url4newpage,
#                 "headline": headline,
#                 "date_of_publication": dateOfPublication,
#                 "main_text": checkMainText ,
#                 #"reports": tweet.find('p', attrs={"class": "shares"}).text.encode('utf-8')
#
#                 # library(stringr)
#                 # str_locate("aaa12xxx", "[0-9]+")
#                 # #      start end
#                 # # [1,]     4   5
#                 # str_extract("aaa12xxx", "[0-9]+")
#                 # # [1] "12"
#
#                 # {"reports": [
#                 #     {   "diseases": 100,
#                 #         "syndrome": "reception",
#                 #         "reported_events": 50,
#                 #         "comments": 75
#                 #     },
#                 # ]},
#             }
#             OutbreakArr.append(outbreakObject)
#             with open('data.json', 'w') as outfile:
#                 json.dump(OutbreakArr, outfile)
#
#             with open('data.json') as json_data:
#                 jsonData = json.load(json_data)
#
#             cur.execute('insert into outbreakTable (url, headline, date, details) values (%s,%s,%s,%s)',(urlAtt,headlineAtt,dopAtt, main_textAtt))
#             db.commit()
#             # cur.execute('select * from outbreakTable')
#             # rows = cur.fetchall()
#             # print('Total Row(s):', cur.rowcount)
#             # for row in rows:
#             #     print(row)
#
# # for i in jsonData:
#     # print "URL: "+ i['url']
#     # print "HEADLINE: "+ i['headline']
#     # print "DATE: " + i['date_of_publication']
#     # print "BODY: "+ i['main_text']
#     # print "\n"
#
#
# cur.execute('select * from outbreakTable')
# rows = cur.fetchall()
# print('Total Row(s):', cur.rowcount)
# for row in rows:
#     print(row)
# db.close()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#



import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
import mysql.connector
from datetime import date
import urllib
#from urllib.request import Request, urlopen


db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Password"
  #auth_plugin="caching_sha2_password"
)

cur = db.cursor()

Tname1 = "outbreakTable"

cur.execute('Create database if not exists cdcDB')
cur.execute('use cdcDB')
# if checkTableExists(db, Tname1) != True:
#     #cur.execute('DROP TABLE IF EXISTS `outbreakTable`')
#     table ='create table if not exists outbreakTable(id int NOT NULL AUTO_INCREMENT, url varchar(300), headline varchar(200), date varchar(20), details varchar(1000), PRIMARY KEY (id))'
#     cur.execute(table)
#     cur.execute('ALTER TABLE outbreakTable AUTO_INCREMENT = 1')
# else:
cur.execute('DROP TABLE IF EXISTS `outbreakTable`')
table ='create table if not exists outbreakTable(id int NOT NULL AUTO_INCREMENT, url varchar(300), headline varchar(200), date varchar(20), details varchar(1000), reported_cases varchar(20), hospitalised_cases varchar(20), deaths varchar(20), PRIMARY KEY (id))'
cur.execute(table)
cur.execute('ALTER TABLE outbreakTable AUTO_INCREMENT = 1')


def fetchNewPages(url):
    response = requests.get(url)
    content = BeautifulSoup(response.content, "html.parser")
    return content;

def fetchHeadline(someHeadline):
    checkHeadline = someHeadline.find("h1", attrs={"id": "content"})
    if checkHeadline != None:
        headlineToFetch = someHeadline.find("h1", attrs={"id": "content"}).text.encode('utf-8')
    else:
        headlineToFetch = "unknown"
    return headlineToFetch

def fetchDate_Time(someDate_Time):
    checkTime = someDate_Time.find("p")

    if checkTime != None:
        checkTime = checkTime.text.encode('utf-8')
    match = re.search(r'\s \d{2}, \d{4}', checkTime)
    match_time1 = re.search(r'\s \d{2}, \d{4} ([Aa]t)? [0-9]?[0-9]\:[0-9]?[0-9](\:[0-9]?[0-9])? ([Aa|Pp][Mm])? (ET|EDT)?', checkTime)

    checkTime = re.sub('[pP]osted ','', checkTime)

    pattern4time = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
    pattern4time1 = '[0-9]?[0-9]\:[0-9]?[0-9](\:[0-9]?[0-9])?'
    matchTime = re.search(pattern4time, checkTime)
    matchTime1 = re.search(pattern4time1, checkTime)

    if matchTime1 is None:
        if matchTime is None:
            except1 = someDate_Time.find('span', attrs={"class": "text-red"})
            if except1 != None:
                pattern4time = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) ([0-9]?[0-9])(,?) ([0-9]{4})'
                matchTime = re.search(pattern4time, except1.text)
                s1 = matchTime.group(0)
                d = datetime.datetime.strptime(s1, '%B %d, %Y')
                paragraph_text = someDate_Time.find("p")
                dateOfPublication = d.strftime('%Y-%m-%d')
                time = "Txx:xx:xx"
                dateOfPublication1 = dateOfPublication + time
                dateOfPublication = dateOfPublication1
            else:
                dateOfPublication = "xx-xx-xxTxx:xx:xx"
        else:
            s1 = matchTime.group(0)
            d = datetime.datetime.strptime(s1, '%B %d, %Y')
            paragraph_text = someDate_Time.find("p")
            dateOfPublication = d.strftime('%Y-%m-%d')
            time = "Txx:xx:xx"
            dateOfPublication = dateOfPublication + time
    else:
            s1 = matchTime.group(0)
            d = datetime.datetime.strptime(s1, '%B %d, %Y')
            dateOfPublication = d.strftime('%Y-%m-%d')
            s2 = matchTime1.group(0)
            s2 = "T" + s2
            dateOfPublication = dateOfPublication + s2
    return dateOfPublication


def mainTextToFetch(mainText):
    checkMainText = mainText.find('div', attrs={"class": "card mb-3"})

    if checkMainText != None:
        checkMainText = checkMainText.text
    else:
        checkMainText = "unknown"
    return checkMainText


def reportedCases(fetchReportedCases):
    let = fetchReportedCases.text

    reported_case = re.search(r'([Rr]eported [Cc]ase(?:s)?): [0-9]+(?:)|([Cc]ase(?:s)?: [0-9]+(?:))', let)
    if reported_case != None:
        checkCase1 = re.search(r'[0-9]+',reported_case.group(0))
        if checkCase1 != None:
            reported_case = checkCase1.group(0)
        else:
            reported_case = "unknown"
    else:
        case2 = re.search(r'(([0-9]+(\,)?[0-9]+) [Cc]ase(?:s)?) | ([Cc]ase(?:s)? ([0-9]+(\,)[0-9]+) | ((Laboratory)? (confirmed)?: ([0-9]+(\,)?[0-9]+)))', let)
        case3 = re.search(r'([0-9]+(\,)?[0-9]+)(\*\*).*[Cc]ase(?:s)?', let)
        if case2 != None:
            checkCase2 = re.search(r'([0-9]+(\,)?[0-9]+)',case2.group(0))
            print checkCase2
            if checkCase2 != None:
                reported_case = checkCase2.group(0)
            else:
                checkCase2 = "unknown"
        else:
            if case3 != None:
                checkCase3 = re.search(r'([0-9]+(\,)?[0-9]+)',case3.group(0))
                reported_case = checkCase3.group(0)
            else:
                reported_case = "unknown"
    return reported_case

def hospitalisedCases(fetchHospitalizedCases):
    let = fetchHospitalizedCases.text
    hospitalized = re.search(r'([Hh]ospitali[zs]ation(?:s)?): [0-9]+(?:)', let)
    if hospitalized != None:
        checkHosp1 = re.search(r'[0-9]+',hospitalized.group(0))
        if hospitalized != None:
            hospitalized =  checkHosp1.group(0)
        else:
            hospitalized = "unknown"
    else:
        hospitalized1 = re.search(r'([0-9]+(\,?)[0-9]+) [Cc]ase(?:s)? |[Cc]ase(?:s)? ([0-9]+(\,)[0-9]+)', let)
        if hospitalized1 != None:
            checkHosp2 = re.search(r'([0-9]+(\,)[0-9]+)',hospitalized1.group(0))
            if checkHosp2 != None:
                hospitalized = checkHosp2.group(0)
            else:
                checkHosp2 = "unknown"
        else:
                hospitalized = "unknown"
    return hospitalized

def reportedDeaths(fetchDeaths):
    let = fetchDeaths.text

    reported_deaths = re.search(r'([0-9]+(\,)?[0-9]?) [Dd]eath(s?)|[Dd]eath(s?): ([0-9]+(\,)?[0-9]?)', let)
    if reported_deaths != None:
        checkCase1 = re.search(r'[0-9]+',reported_deaths.group(0))
        if checkCase1 != None:
            reported_deaths = checkCase1.group(0)
        else:
            reported_deaths = "unknown"
    else:
            reported_deaths = "unknown"
    return reported_deaths

content = fetchNewPages('https://www.cdc.gov/outbreaks/')

OutbreakArr = []
usBasedBox = content.find('div', attrs={"class": "card-body bg-tertiary"})
bulletPoints = usBasedBox.find('ul', attrs={"class": "list-bullet feed-item-list"})

glueIt = "https://www.cdc.gov"
somethingHTM = ""
pattern = re.compile("^https")

for outbreaks in bulletPoints.findAll('li'):
    #get the url
    urls = outbreaks.find('a')
    if urls == None:
        urls = glueIt + urls

    if urls != None:
        url4newpage = urls.get('href')

        #if re.search(r'.*\.html$', url4newpage) == None:
        #    print "--------------------------------------------"
            #req = urllib.request.Request(url4newpage)
            #with urllib.request.urlopen(req) as response:
            #    newPageContent = response.read()

            #print urls.text
            #print newPageContent

        if pattern.match(url4newpage) == None:
            url4newpage = glueIt + url4newpage

        if pattern.match(url4newpage):
            #get the new url
            newPageContent = fetchNewPages(url4newpage)

            #get the headline
            headline = fetchHeadline(newPageContent)

            #get the date and time
            dateOfPublication = fetchDate_Time(newPageContent)

            #get the body
            checkMainText = mainTextToFetch(newPageContent)

            #get the number of reported cases
            reported_case = reportedCases(newPageContent)

            #get the number of hospitalized people
            hospitalised = hospitalisedCases(newPageContent)

            #get the number of fetchDeaths
            deaths = reportedDeaths(newPageContent)

    else:
        url = "unknown"

    urlAtt = url4newpage
    headlineAtt = headline
    dopAtt = dateOfPublication
    main_textAtt = checkMainText
    reported_casesAtt = reported_case
    hospitalizedAtt = hospitalised
    deathsAtt = deaths

    cur.execute('insert into outbreakTable (url, headline, date, details, reported_cases, hospitalised_cases, deaths) values (%s,%s,%s,%s,%s,%s,%s)',(urlAtt,headlineAtt,dopAtt, main_textAtt, reported_casesAtt, hospitalizedAtt, deathsAtt))
    db.commit()
    outbreakObject = {

        "url": url4newpage,
        "headline": headline,
        "date_of_publication": dateOfPublication,
        "main_text": checkMainText,
        "reported_cases": reported_case,
        "hospitalised" : hospitalised,
        "death" : deaths

    }
    OutbreakArr.append(outbreakObject)
    with open('data.json', 'w') as outfile:
        json.dump(OutbreakArr, outfile)

    with open('data.json') as json_data:
        jsonData = json.load(json_data)


cur.execute('select * from outbreakTable')
rows = cur.fetchall()
print('Total Row(s):', cur.rowcount)
for row in rows:
    print(row)

# for i in jsonData:
#     print "URL: "+ i['url']
#     print "HEADLINE: "+ i['headline']
#     print "DATE: " + i['date_of_publication']
#     print "BODY: "+ i['main_text']
#     print "REPORTED CASES: "+ i['reported_cases']
#     print "HOSPITALISED CASES: "+ i['hospitalised']
#     print "DEATHS: "+ i['death']
#     print "\n"

db.close()
