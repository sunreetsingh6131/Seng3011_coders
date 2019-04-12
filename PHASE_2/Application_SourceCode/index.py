from flask import Flask, request, Response, jsonify
from flask_restplus import Api, Resource , fields
import datetime , re
import json, os, time, decimal, re, subprocess,random,string
from bottle import HTTPResponse
from flask_api import status
import logging

import mysql.connector
app=Flask(__name__)
api = Api(app)


# connect to our database
db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Password"
    )
cur = db.cursor()
cur.execute('use cdcDB')


def locationCheck(place):
    for line in open("StatesUS.txt"):
        nLine = line.rstrip()
        place = make_string(place)
        if place.lower() == nLine.lower():
            return True

    return False

def keyCheck(place):

    for line in open("diseasesList.txt"):
        nLine = line.rstrip()
        place = make_string(place)
        if place.lower() == nLine.lower():
            return True

    return False

def checkDate(dates):
    dates = make_string(dates)

    if re.match('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}T[0-9]{2}:[0-9]{2}:[0-9]{2}',dates) is None :
        print("---"+dates)
        return False
    return True




# function used to split a date strting
def getDateInParts(inputs):
    inputs = make_string(inputs)
    if re.search('^x', inputs):
        return 1769,1 ,1,0,0,0
    s_year = re.search('^\w{4}-' , inputs).group()
    inputs = inputs.replace(s_year, "")
    s_year = re.search('^\w{4}' , s_year).group()
    s_month = re.search('^\w{2}-', inputs).group()
    inputs = inputs.replace(s_month, "")
    s_month = re.search('^\w{2}', s_month).group()
    s_date = re.search('\w{2}T', inputs).group()
    inputs = inputs.replace(s_date, "")
    s_date = re.search('\w{2}', s_date).group()
    s_hour = re.search('^\w{1,2}:', inputs).group()
    inputs = inputs.replace(s_hour, "")
    s_hour = s_hour.replace(':', '')
    s_min = re.search('^\w\w', inputs).group()
    inputs = inputs.replace(s_min, "")
    s_sec = re.search(':\w\w$', inputs)
    if s_sec is None :
        s_sec = 0
    else:
        s_sec = s_min.replace(':','')

    return s_year, s_month ,s_date, s_hour, s_min , s_sec


def make_string(words):
    s = ""
    for i in words:
        s = s+ i
    return s


log = logging.getLogger(__name__)

ns = api.namespace('outbreaktable', description='Returns the analysis after getting the data from CDC')

@api.doc(params={'start_date': 'start of period of interest. example-> 2019-02-15T03:00:00'})
@api.doc(params={'end_date': 'end of period of interest. example: 2019-02-25T03:00:00'})

@ns.route('/show/<string:start_date>/<string:end_date>/<string:location>/<string:key_terms>')
<<<<<<< HEAD
@ns.route('/show/<string:start_date>/<string:end_date>//<string:key_terms>')
@ns.route('/show/<string:start_date>/<string:end_date>/<string:location>')
=======

>>>>>>> a0f3b45b28beddbe37df3de070e3b5d354ea2f94
@ns.route('/show/<string:start_date>/<string:end_date>')
@api.response(404, 'database not found.')
@api.response(400, 'Invalid inputs.')
class show(Resource):

    @api.response(200, 'Data found and analysis shown.')
    def get(self,start_date,end_date, location="all",key_terms='all'):
        print(start_date)

        #  if location != all then check the validity of the location
        if location != 'all':
            loc1 = re.split(',', location)
            for i in loc1:
                if locationCheck(i) is False:
                    res = {
                        "details": "location incorrect"
                    }
                    return res, status.HTTP_400_BAD_REQUEST


        if key_terms != 'all':
            key = re.split(',',key_terms)
            for i in key:
                if keyCheck(i) is False:
                    res = {
                        "details": "key word incorrect"
                    }
                    return res, status.HTTP_400_BAD_REQUEST

        if checkDate(start_date) is False :
            res = {
                 "details": "date incorrect",
                 "correct_example" : "2019-05-19T16:45:38"
            }
            return res, status.HTTP_400_BAD_REQUEST
        if checkDate(end_date) is False :
            res = {
                 "details": "date incorrect",
                 "correct_example" : "2019-05-19T16:45:38"
            }
            return res, status.HTTP_400_BAD_REQUEST
        print(end_date)

         # splitted the date string
        s_year, s_month ,s_day, s_hour, s_min , s_sec = getDateInParts(start_date)
        s_date = datetime.datetime(int(s_year), int(s_month), int(s_day), int(s_hour), int(s_min), int(s_sec))


        e_year, e_month ,e_day, e_hour, e_min , e_sec = getDateInParts(end_date)
        e_date = datetime.datetime(int(e_year), int(e_month), int(e_day), int(e_hour), int(e_min), int(e_sec))

        # Checking is the start_date is less than the end_date
        if s_date > e_date :
            res = {
            'details':"incorrect inputs"
            }
            return res , status.HTTP_400_BAD_REQUEST

         # Querry the database for all outputs
        querry = "SELECT * from outbreakTable"
        cur.execute(querry)
        result_rows = cur.fetchall()

        data=[]
        for row in result_rows:
            # For each word in key term check if it is in title/headline

            #  we need to split the key terms and store it in the array
            key_terms = make_string(key_terms)
            if key_terms == 'all':
                key_terms1 = ""
            else :
                key_terms1 = re.split(',', key_terms)

            isSubstring = True;
            for word in key_terms1:
                # If term not substring of headline break
                if word.lower() not in row[2].lower():
                    isSubstring = False;
                    break

            # If not all keywords are substring of headline goto next row
            if isSubstring == False:
                continue

            g_year, g_month ,g_day, g_hour, g_min , g_sec = getDateInParts(row[3])
            if (g_hour == "xx"):
                g_hour = 0
                g_min = 0
                g_sec = 0
            givenDate = datetime.datetime(int(g_year), int(g_month), int(g_day), int(g_hour), int(g_min), int(g_sec))

            if (givenDate < s_date or givenDate > e_date):
                continue
            location = make_string(location)
            if location == 'all':
                location1 = ""
            else:
                location1 = re.split(',', location)
            isIt = False
            if location1 == "":
                isIt = True
            for i in location1:
                if i.lower() in row[8].lower():
                    isIt = True

            if isIt is False:
                continue

            report = {
                        'disease': row[9],
                        'syndrome': row[10],
                        'reported events': row[5],
                        'hospitalised' : row[6],
                        'deaths' : row[7],
                        'locations' : row[8]
            }
            item ={
                "url": row[1],
                "headline": row[2],
                "date_of_publication": row[3],
                "main_text": row[4],
                'reports' : [report]

            }

            # Fill dictionary with items
            # item = json.dumps(item)
            # data = data + str(item)
            data.append(item)
            print(data)


        datax = []
        if data == datax:
            return {
                "details" : "data not found"
            }, status.HTTP_404_NOT_FOUND

        sample_result = data
        return sample_result , status.HTTP_200_OK

# this is the main file
#########################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
