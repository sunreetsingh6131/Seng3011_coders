from flask import Flask, request, Response, jsonify
#from newsapi import NewsApiClient
#84ceb92e06b44f1db554d716c0fa0a01 API KEY
from flask_restplus import Api, Resource , fields
from flask_cors import CORS
import datetime , re
import json, os, time, decimal, re, subprocess,random,string
from bottle import HTTPResponse
from flask_api import status
import logging
import mysql.connector

app=Flask(__name__)
CORS(app)
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

    for line in open("keysearchterms.txt"):
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
    if words != None:
        s = ""
        for i in words:
            s = s+ i
        return s


log = logging.getLogger(__name__)

ns = api.namespace('outbreaktable', description='Returns the analysis after getting the data from CDC')
#@api.doc(params={'start_date': 'start of period of interest. example-> 2019-02-15T03:00:00'})
@api.route('/show', methods=['GET'])
@api.doc(params={'keyterm': 'example: keyterm = measles'})
@api.doc(params={'location': 'example: location = New York'})
@api.doc(params={'end_date': 'end of period of interest. example: 2019-02-25T03:00:00'}, required=True)
@api.doc(params={'start_date': 'start of period of interest. example: 2019-02-15T03:00:00'}, required=True)


# @ns.route('/show/<string:start_date>/<string:end_date>/<string:location>/<string:key_terms>')
# #@cross_origin()
#
# @ns.route('/show/<string:start_date>/<string:end_date>/<string:key_terms>')
# #@cross_origin()
# @ns.route('/show/<string:start_date>/<string:end_date>/<string:location>')
# #@cross_origin()
#
# @ns.route('/show/<string:start_date>/<string:end_date>')
#@cross_origin()
@api.response(404, 'database not found.')
@api.response(400, 'Invalid inputs.')

# @app.route('/show')
# def query_example():
#     keyTerm = request.args.get('keyterm') #if key doesn't exist, returns None
#     location = request.args['location'] #if key doesn't exist, returns a 400, bad request error
#     startDate = request.args.get('start_date')
#     endDate = request.args.get('end_date')
# print request.args
# >> {"arg1": "hello", "arg2": "world"}

class show(Resource):

    @api.response(200, 'Data found and analysis shown.')
    def get(self):

        #location = request.args.['location'] #if key doesn't exist, returns a 400, bad request error
        key_terms = request.args.get('keyterm') #if key doesn't exist, returns None
        location = request.args.get('location') #if key doesn't exist, returns a 400, bad request error
        start_date = request.args.get('start_date')
        # if start_date == None:
        #     res = {
        #          "details": "Field can't be left empty",
        #     }
        #     return res, status.HTTP_400_BAD_REQUEST
        end_date = request.args.get('end_date')
        # if end_date == None:
        #     res = {
        #          "details": "Field can't be left empty",
        #     }
        #     return res, status.HTTP_400_BAD_REQUEST
        #  if location != all then check the validity of the location

        if location != None:
            #print("here")
            if location != 'all':
                loc1 = re.split(',', location)
                for i in loc1:
                    if locationCheck(i) is False:
                        res = {
                            "details": "location incorrect"
                        }
                        return res, status.HTTP_400_BAD_REQUEST


        if key_terms != None:
            if key_terms != 'all':
                key = re.split(', ',key_terms)
                for i in key:
                    if keyCheck(i) is False:
                        res = {
                            "details": "keyterms incorrect"
                        }
                        return res, status.HTTP_400_BAD_REQUEST


        if start_date != None:
            if checkDate(start_date) is False :
                res = {
                     "details": "date incorrect",
                     "correct_example" : "2019-05-19T16:45:38"
                }
                return res, status.HTTP_400_BAD_REQUEST


        if end_date != None:
            if checkDate(end_date) is False :
                res = {
                     "details": "date incorrect",
                     "correct_example" : "2019-05-19T16:45:38"
                }
                return res, status.HTTP_400_BAD_REQUEST

        # splitted the date string
        if start_date !=None:
            s_year, s_month ,s_day, s_hour, s_min , s_sec = getDateInParts(start_date)
            s_date = datetime.datetime(int(s_year), int(s_month), int(s_day), int(s_hour), int(s_min), int(s_sec))
            cs_date= datetime.datetime(int(s_year), int(s_month), int(s_day))

        if end_date!=None:
            e_year, e_month ,e_day, e_hour, e_min , e_sec = getDateInParts(end_date)
            e_date = datetime.datetime(int(e_year), int(e_month), int(e_day), int(e_hour), int(e_min), int(e_sec))
            ce_date = datetime.datetime(int(e_year), int(e_month), int(e_day))

        # Checking is the start_date is less than the end_date
        #console.log(e_date)

        # print(s_date)
        # print(e_date)

        # if start_date == None or end_date == None:
        #     res = {
        #          "details": "date fields can't be left empty",
        #     }
        #     return res , status.HTTP_400_BAD_REQUEST

        if start_date !=None or end_date != None:
            if cs_date > ce_date :
                res = {
                'details':"invalid start date and end date"
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
            if key_terms != None:
                key_terms = make_string(key_terms)
                if key_terms == None:
                    #print('here')
                    key_terms1 = ""
                else :
                    key_terms1 = re.split(', ', key_terms)
                    #print(key_terms1)

                isSubstring = False;
                for word in key_terms1:
                    # print("my input ->"+word)
                    # print("row in database-> "+row[11])
                    if word.lower() in row[11].lower():
                        isSubstring = True;
                        # print("yesyesyes")
                        break #break

                # code below unreachable not using keyterms always.
                if isSubstring == False:
                    continue

            if start_date != None:
                g_year, g_month ,g_day, g_hour, g_min , g_sec = getDateInParts(row[3])
                if (g_hour == "xx"):
                    g_hour = 0
                    g_min = 0
                    g_sec = 0
                givenDate = datetime.datetime(int(g_year), int(g_month), int(g_day), int(g_hour), int(g_min), int(g_sec))

                if (givenDate < s_date or givenDate > e_date):
                    continue

            if location != None:
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

            # type1 = None
            # type2 = None
            # type3 = None

            reportedArr = []

            type = [None, None, None]
            no = [0, 0, 0]
            # print(row[6])
            if row[5] != 'unknown':
                if row[5] != None:
                    if int(row[5]) > 0:
                        type[0] = "infected"
                        no[0] = row[5]
            if row[6] != 'unknown':
                if row[6] != None:
                    if int(row[6]) > 0:
                        type[1] = "hospitalised"
                        no[1] = row[6]
            if row[7] != 'unknown':
                if row[7] != None:
                    if int(row[7]) > 0:
                        type[2] = "death"
                        no[2] = row[7]

            if row[8] != None:
                if type[0] == None and type[1] == None and type[2] == None:
                    reported = {
                        'type': "presence",
                        'date': row[3],
                        'location': row[8],
                        'number_affected': "unknown"
                    }
                    reportedArr.append(reported)




            # 'hospitalised' : row[6],
            # 'deaths' : row[7],
            # 'locations' : row[8]


            i = 0
            while i < 3:
                if type[i] != None:
                    reported = {
                        'type': type[i],
                        'date': row[3],
                        'location': row[8],
                        'number_affected': no[i]
                    }
                    reportedArr.append(reported)
                i=i+1


            if len(reportedArr) == 0:
                reported = {
                    'type': "",
                    'date': "",
                    'location': "",
                    'number_affected': ""
                }
                reportedArr.append(reported)


            report = {
                        'disease': row[9],
                        'syndrome': row[10],
                        'reported_events': reportedArr,
                        'comments' : "null"
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
            # for x in data:
            #     print(x)

            # print(item)
            #print('\n'.join(data))
            #print(data)
            #json_data = json.dumps(data)


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
