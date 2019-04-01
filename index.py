from flask import Flask, request, Response
from flask_restplus import Api, Resource , fields
import datetime , re
import json, os, time, decimal, re, subprocess,random,string

app=Flask(__name__)
api = Api(app)


# function used to split a date strting
def getDateInParts(inputs):
    s_year = re.search('^[0-9]{4}-' , inputs).group()
    s_year = re.search('^[0-9]{4}' , s_year).group()
    s_date = re.search('-[0-9]{2}-', inputs).group()
    s_date = re.search('[0-9]{2}', s_date).group()
    s_month = re.search('-[0-9]{2}T', inputs).group()
    s_month = re.search('[0-9]{2}', s_month).group()
    s_hour = re.search('T[0-9]{2}:', inputs).group()
    s_hour = re.search('[0-9]{2}', s_hour).group()
    s_min = re.search(':[0-9]{2}:', inputs).group()
    s_min = re.search('[0-9]{2}', s_min).group()
    s_sec = re.search(':[0-9]{2}$', inputs).group()
    s_sec = re.search('[0-9]{2}', s_sec).group()
    return s_year, s_date ,s_month, s_hour, s_min , s_sec



@api.route('/show')
class show(Resource):
    
    def get(self):
        
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
        s_year, s_date ,s_month, s_hour, s_min , s_sec = getDateInParts(inputs['start_date'])
        # start_date = datetime.datetime(s_year, s_date ,s_month, s_hour, s_min , s_sec)
        e_year, e_date ,e_month, e_hour, e_min , e_sec = getDateInParts(inputs['end_date'])
        # end_date = datetime.datetime(s_year, s_date ,s_month, s_hour, s_min , s_sec)

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

        cur.execute('SELECT * from outbreakTable WHERE details LIKE %(%s)% AND date BETWEEN (%s) and (%s)', location, s_date, e_date)
        result_rows = cur.fetchall()
       
        sample_result = {}

        for row in result_rows:
            # For each word in key term check if it is in title/headline
            isSubstring = True;
            for word in key_terms
                # If term not substring of headline break
                if word not in row[1]:
                    isSubstring = False;
                    break
            
            # If not all keywords are substring of headline goto next row
            if isSubstring == False:
                continue

            # row[0]=url,row[1]=headline,row[2]=date_of_publication,row[3]=main_text
            # Create dictionary
            data=[]
            item = {                
                "url": row[0],
                "headline": row[1],
                "date_of_publication": row[2],
                "main_text": row[3], 
            }

            # Fill dictionary with items
            data.append(item)

        # Append to json object
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
