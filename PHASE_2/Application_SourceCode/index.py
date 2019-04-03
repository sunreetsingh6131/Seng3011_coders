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
        passwd=""
    )
cur = db.cursor()
cur.execute('use cdcDB')




# function used to split a date strting
def getDateInParts(inputs):
    s_year = re.search('^[0-9]{4}-' , inputs).group()
    inputs = inputs.replace(s_year, "")
    s_year = re.search('^[0-9]{4}' , s_year).group()
    s_month = re.search('^[0-9]{2}-', inputs).group()
    inputs = inputs.replace(s_month, "")
    s_month = re.search('^[0-9]{2}', s_month).group()
    s_date = re.search('[0-9]{2}T', inputs).group()
    inputs = inputs.replace(s_date, "")
    s_date = re.search('[0-9]{2}', s_date).group()
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

    return s_year, s_month ,s_date, s_hour, s_min , s_sec



log = logging.getLogger(__name__)

ns = api.namespace('outbreaktable', description='Returns the analysis after getting the data from CDC')

@ns.route('/show/<string:location>,<string:key_terms>,<string:start_date>,<string:end_date>')
@api.response(404, 'database not found.')
@api.response(400, 'Invalid inputs.')
class show(Resource):

    @api.response(200, 'Data found and analysis shown.')
    def get(self,location,key_terms,start_date,end_date):

        if location == "" and key_terms is "":
            res = {
                'message': "input incorrect"
                }
            return jsonify(res),status.HTTP_400_BAD_REQUEST

        # checking if the format of the date is correct
        prog = re.compile('^%d{4}.%d{2}.%d{2}T%d:{2}:%x{2}:%x{2}$')
        input = False
        if prog.match(start_date) and prog.match(end_date):
                input = True;

        if input is False:
            res = {
                'message': "input incorrect"
                }
            return res,status.HTTP_400_BAD_REQUEST

         # splitted the date string
        s_year, s_month ,s_day, s_hour, s_min , s_sec = getDateInParts(start_date)
        s_date = datetime.datetime(int(s_year), int(s_month), int(s_day), int(s_hour), int(s_min), int(s_sec))


        e_year, e_month ,e_day, e_hour, e_min , e_sec = getDateInParts(end_date)
        e_date = datetime.datetime(int(e_year), int(e_month), int(e_day), int(e_hour), int(e_min), int(e_sec))

        # Checking is the start_date is less than the end_date
        if s_date > e_date :
            res = {
            'details':"incorrect input"
            }
            return res , status.HTTP_400_BAD_REQUEST

        

        return jsonify({
                'message' : location,
                'massage' : start_date
        })

# this is the main file
#########################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
