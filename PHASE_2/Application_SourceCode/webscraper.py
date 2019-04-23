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
table ='create table if not exists outbreakTable(id int NOT NULL AUTO_INCREMENT, url varchar(300), headline varchar(200), date varchar(20), details varchar(1000), reported_cases varchar(20), hospitalised_cases varchar(20), deaths varchar(20), location varchar(500), disease varchar(50), syndrome varchar(50), keyterms varchar(100), PRIMARY KEY (id))'
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

def locationCheck(fetchPage):
    page = fetchPage.text
    sList = []
    for line in open("StatesUS.txt"):
        nLine = line.rstrip()
        myRegex = r""+re.escape(nLine)+""
        matchObj = re.search( myRegex, page, re.M|re.I)
        if matchObj:
            sList.append(nLine)

    return sList


def syndromeCheck(fetchPage):
    page = fetchPage.text
    sList = []
    for line in open("syndromeList.txt"):
        nLine = line.rstrip()
        myRegex = r""+re.escape(nLine)+""
        matchObj = re.search(myRegex, page, re.M|re.I)
        if matchObj:
            sList.append(nLine)

    #print sList
    return sList


def termsCheck(fetchPage):
    page = fetchPage.text
    sList = []
    for line in open("keysearchterms.txt"):
        nLine = line.rstrip()
        myRegex = r""+re.escape(nLine)+""
        matchObj = re.search(myRegex, page, re.M|re.I)
        if matchObj:
            sList.append(nLine)

    #print sList
    return sList

def diseasesCheck(fetchPage):
    page = fetchPage.text
    sList = []
    for line in open("diseasesList.txt"):
        nLine = line.rstrip()
        myRegex = r""+re.escape(nLine)+""
        matchObj = re.search(myRegex, page, re.M|re.I)
        if matchObj:
            sList.append(nLine)
    return sList

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

            #location lists
            locations = locationCheck(newPageContent)

            #diseases
            diseases = diseasesCheck(newPageContent)

            #syndrome
            syndromes = syndromeCheck(newPageContent)

            #terms
            keytermsList = termsCheck(newPageContent)
    else:
        url = "unknown"

    urlAtt = url4newpage
    headlineAtt = headline
    dopAtt = dateOfPublication
    main_textAtt = checkMainText
    reported_casesAtt = reported_case
    hospitalizedAtt = hospitalised
    deathsAtt = deaths

    #locationAtt = locations
    locationAtt = ", ".join(locations)
    diseasesAtt = ", ".join(diseases)

    syndromeAtt = ", ".join(syndromes)
    ktAtt = ", ".join(keytermsList)

    print ktAtt

    cur.execute('insert into outbreakTable (url, headline, date, details, reported_cases, hospitalised_cases, deaths, location, disease, syndrome, keyterms) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(urlAtt,headlineAtt,dopAtt, main_textAtt, reported_casesAtt, hospitalizedAtt, deathsAtt, locationAtt, diseasesAtt, syndromeAtt, ktAtt))
    db.commit()
    # outbreakObject = {
    #
    #     "url": url4newpage,
    #     "headline": headline,
    #     "date_of_publication": dateOfPublication,
    #     "main_text": checkMainText,
    #     "reported_cases": reported_case,
    #     "hospitalised" : hospitalised,
    #     "death" : deaths,
    #     "location" : locations,
    #     "disease" : diseasesAtt,
    #     "syndrome" : syndromeAtt
    # }
    # OutbreakArr.append(outbreakObject)
    # with open('data.json', 'w') as outfile:
    #     json.dump(OutbreakArr, outfile)
    #
    # with open('data.json') as json_data:
    #     jsonData = json.load(json_data)

    #print locations
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
#     #print "locations: " + i['locations']
#     print "\n"

db.close()

