from flask import Flask, request, Response
from flask_restplus import Api, Resource , fields
import datetime , re
import json, os, time, decimal, re, subprocess,random,string
from bottle import HTTPResponse
from flask_api import status

import mysql.connector

app=Flask(__name__)
api = Api(app)


# function used to split a date strting
def getDateInParts(inputs):
    s_year = re.search('^[0-9]{4}-' , inputs).group()
    inputs = inputs.replace(s_year, "")
    s_year = re.search('^[0-9]{4}' , s_year).group()
    s_date = re.search('^[0-9]{2}-', inputs).group()
    inputs = inputs.replace(s_date, "")
    s_date = re.search('^[0-9]{2}', s_date).group()
    s_month = re.search('[0-9]{2}T', inputs).group()
    inputs = inputs.replace(s_month, "")
    s_month = re.search('[0-9]{2}', s_month).group()
    s_hour = re.search('^\w\w:', inputs).group()
    inputs = inputs.replace(s_hour, "")
    s_hour = s_hour.replace(':', '')
    s_min = re.search('^\w\w', inputs).group()
    inputs = inputs.replace(s_min, "")
    s_sec = re.search(':\w\w$', inputs)
    if s_sec is None :
        s_sec = 0
    else:
        s_sec = s_min.replace(':','')

    return s_year, s_date ,s_month, s_hour, s_min , s_sec



@api.route('/show')
class show(Resource):

    def get(self):

        inputs = request.get_json()
        location = inputs['location']
        #  now key terms are a array
        # Edge Case 1 :
        if location == "" and inputs['key_terms'] is "":
            res = {
                'status_code': 400,
                'details': "input incorrect"
                }
            return res,status.HTTP_400_BAD_REQUEST


        key_terms = inputs['key_terms']
        key_terms = re.split(',', key_terms)
        ##########################################
        # Get the Date
        s_date = inputs['start_date']
        e_date = inputs['end_date']
        ##########################################
        # splitted the date string
        s_year, s_month ,s_day, s_hour, s_min , s_sec = getDateInParts(inputs['start_date'])
        # start_date = datetime.datetime(s_year, s_date ,s_month, s_hour, s_min , s_sec)
        start_date = s_year + "." +s_month + "." + s_date + " "+ s_hour + ":"+ s_min + ":" +s_sec
        s_date = datetime.datetime(int(s_year), int(s_month), int(s_day), int(s_hour), int(s_min), int(s_sec))
        e_year, e_month ,e_day, e_hour, e_min , e_sec = getDateInParts(inputs['end_date'])
        # end_date = datetime.datetime(s_year, s_date ,s_month, s_hour, s_min , s_sec)
        end_date = e_year + "." +e_month + "." + e_day + " "+ e_hour + ":"+ e_min + ":" +e_sec
        e_date = datetime.datetime(int(e_year), int(e_month), int(e_day), int(e_hour), int(e_min), int(e_sec))
        # start_date = datetime.datetime()
        ###############################################################################################################################
        # connect to our database
        db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="Password"
        )

        cur = db.cursor()
        cur.execute('use cdcDB')
        querry = "SELECT * from outbreakTable"
        # print(querry)
        # cur.execute('SELECT * from outbreakTable WHERE details LIKE (%s) AND date BETWEEN (%s) and (%s)', s_date, e_date)
        cur.execute(querry)
        result_rows = cur.fetchall()

        data=[]
        for row in result_rows:
            # For each word in key term check if it is in title/headline
            isSubstring = True;
            for word in key_terms:
                # If term not substring of headline break
                if word.lower() not in row[2].lower():
                    isSubstring = False;
                    break

            # If not all keywords are substring of headline goto next row
            if isSubstring == False:
                continue

            # now we need to check for the dates
            g_year, g_month ,g_day, g_hour, g_min , g_sec = getDateInParts(row[3])
            if (g_hour == "xx"):
                g_hour = 0
                g_min = 0
                g_sec = 0
            givenDate = datetime.datetime(int(g_year), int(g_month), int(g_day), int(g_hour), int(g_min), int(g_sec))

            if (givenDate < s_date or givenDate > e_date):
                continue
            # row[0]=url,row[1]=headline,row[2]=date_of_publication,row[3]=main_text
            # Create dictionary
            item ={
                "url": row[1],
                "headline": row[2],
                "date_of_publication": row[3],
                "main_text": row[4],
            }

            # Fill dictionary with items
            data.append(item)

        # Append to json object
        datax = []
        if data == datax:
            return {
                "details" : "data not found"
            }, status.HTTP_404_NOT_FOUND
        sample_result = json.dumps(data)

        ##################################################################################################################################

        # sample_result = {
        #     'url':"www.cdc.gov/salmonella/typhimurium-01-09/index.html",
  #           'date_of_publication':"2019-01-25",
  #           'headline':"Outbreak of Salmonella infections linked to pet hedgehogs ",
  #           'main_text':"CDC and public health officials are investigating a multistate outbreak of salmonella infections linked to pet hedgehog ",
  #           'reports': "NULL"
        #  }

        return sample_result , status.HTTP_200_OK


# this is the main file
#########################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
