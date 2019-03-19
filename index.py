from flask import Flask, request, Response
from pymongo import MongoClient
import json, os, time, decimal, re, subprocess,random,string
from flask_cors import CORS
from flask_restful.utils.cors import crossdomain

app = Flask(__name__)
CORS(app)
client = MongoClient(host="mongodb://<amol>:<amoljain1>@ds117806.mlab.com:17806/seng3011")
db = client["3011project"]

#######################################################
def save_user(name, password, email):
    if find_user(name) == "-1":
        db.users.insert_one({"name":name,"password":password,"email":email})
        return '0'
    else:
        return '-1'

########################################################
@app.route("/register", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def register():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password') and \
            request.form.get('email'):
        datax = request.form.to_dict()
        usernamx = datax.get("username")
        passwordx = datax.get("password")
        emailx = datax.get("email")
        # print(datax)
        res = save_user(usernamx, passwordx, emailx)
        if res == "0":
            print('OKAY')
            return Response(json.dumps({'message': 'User Creation successful'}), status=200)
        else:
            print('No')
            return Response(json.dumps({'message': 'User Creation failed'}), status=400)
    else:
        return Response(json.dumps({'message': 'Missing arguments'}), status=400)



##############################################################
def find_user(name):
    ress = db.users.find_one({"name": name})
    # print(ress.get("name"))
    # username = ress.get("name")
    # password = ress.get("password")
    # user_info = [username,password]
    # print(user_info[0])
    # print(ress)
    if ress is not None:
        # print('222')
        user_info = [ress.get("name"), ress.get("password")]
        return user_info
    else:
        # print('-1+1')
        return "-1"




#####################################################################
@app.route('/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def login():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        datax = request.form.to_dict()
        usernamx = datax.get("username")
        passwordx = datax.get("password")
        print(usernamx, passwordx)
        res = find_user(usernamx)
        # format of res is [username, password]
        print(res[0])
        if res == "-1":
            print('-1')
            # return {'status': "user not found"}, status.HTTP_404_NOT_FOUND
            return Response(json.dumps({'message': "user not found"}), status=404, mimetype='application/json')
        elif passwordx != res[1]:
            print("0")
            return Response(json.dumps({'message': 'password incorrect'}), status=401, mimetype='application/json')
        else:
            key = generateKey()
            return Response(json.dumps({'username': usernamx, 'key': key}), status=200, mimetype='application/json')
    else:
        return Response({}, status=400, mimetype='application/json')



#########################################################################
if __name__ == '__main__':
    app.run()