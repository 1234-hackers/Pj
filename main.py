
import base64
from email import message
#from turtle import st
import shutil
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from dns.message import Message
from flask import Flask, render_template, url_for, request, redirect,flash,session,jsonify

from flask_pymongo import PyMongo
from flask_wtf.form import FlaskForm
from pymongo import MongoClient
import passlib
from passlib.context import CryptContext
from passlib.hash import bcrypt_sha256,argon2,ldap_salted_md5,md5_crypt
import time
from datetime import  datetime as dt
import smtplib
from email.message import EmailMessage
import socket,os
from functools import wraps
from bson import ObjectId
#from flask_hcaptcha import hCaptcha
from flask_wtf import RecaptchaField,FlaskForm
from wtforms.validators import EqualTo, InputRequired
from flask_wtf.csrf import CSRFProtect,CSRFError
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
import email_validator 
import random
import requests
import base64
from bson.binary import Binary
import markupsafe
from markupsafe import escape , Markup

from pymongo import MongoClient
from pymongo.server_api import ServerApi

import secrets
import os


WTF_CSRF_SECRET_KEY = "kkdrkdooxoor38e88dixjrjsk"
uri = "mongodb+srv://jackson:mutamuta@hbcall.ihz6j.azure.mongodb.net/test?retryWrites=true&w=majority" 
 # Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
application = Flask(__name__)

#captcha


application.config['HCAPTCHA_ENABLED'] =  False

application.config ["HCAPTCHA_SITE_KEY"]  =  "hsite"

application.config ['HCAPTCHA_SECRET_KEY'] = "hsec"

SECRET_KEY = "dsfdsjgdjgdfgdfgjdkjgdg"
csrf = CSRFProtect(application)


#mongoDB configs
#application.config['MONGO_DBNAME'] = 'users'
# application.config['MONGO_URI'] = 'mongodb://'+ipst+':27017/users'
#application.config['MONGO_URI'] = 'mongodb://localhost:27017/main'

#mongo = PyMongo(application)


application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

Hash_passcode = CryptContext(schemes=["sha256_crypt" ,"des_crypt"],sha256_crypt__min_rounds=131072)

#mongo = PyMongo(application)

users = client.bet.users
pools = client.bet.pool_tables
verif = client.bet.verify_email
ips = client.bet.ips
dates = client.bet.dates


def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "login_user" in session:
            return f(*args,**kwargs,)
        else:
            time.sleep(2)
            return redirect(url_for('login'))
    return wrap


def send_mail(rec,code):
    recipient = rec
    code = code
    email_body = """
<!DOCTYPE html>
<html>
<head>
<title>Email Confirmation</title>
</head>
<body style ="font-size: 20px;">
<p>You have received this email because it was used to create an account.If
this wasn't you please ignore it.

<br>
{}
</p>

</p>
</body>
</html>
     """.format(code)

    email_command = f'mail -a "Content-Type: text/html" -s "Appreciation" {recipient} <<EOF'
    full_email = email_command + email_body
    os.system(full_email)
    return 'ok'

@application.route('/rec',methods = ["POST"])
def rec():
     if request.method == 'POST':
          dt = request.form.get()
          print(dt)

     return "done"

@application.route('/create_file', methods=["POST","GET"])
def create_file():
     if request.method == 'POST':
          with open(f"{request.form.get('name')}.txt", "w") as f:
               f.write('FILE CREATED AND SUCCESSFULL POST REQUEST!')
     return render_template("index.html")


@application.route('/deposit')
def deposit():

    return render_template('deposit.html')



@application.route('/profile')
def profile():

    return render_template('profile.html')



@application.route('/submit', methods=["POST"])
def submit():

    name = session['login_user']
    try:
        csrf_token = request.headers.get("X-CSRFToken")

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received or invalid JSON'}), 400

        print("Parsed JSON:", data)
        print(name)
        users.find_one({"email":name})
        response = {'message': 'Form data received successfully!', 'data': data}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return redirect(url_for("home"))
@application.route('/',methods = ["POST","GET"])
@login_required
def home():
     gh=[]
     names = ['james','mark','pinchez']
     b_id =  secrets.token_hex(13)
     bid = secrets.token_hex(12)
     dag = 5
     jmp = [bid]
     now = dt.now()
     now_c = now.strftime(" %Y:%m:%d ")
     timez = now_c
     result = []
     k3 = [1,2,3]

     #div = result
     div = random.choice(k3)
     poolz =len(list( pools.find({"day":timez}) ))
     if poolz <  5:
          pools.insert_one({"p_num" : random.randint(345849,5838392) , "ln":div,
          "player":jmp,"day": timez  })
          poolzy = pools.find({"day":timez})
          for x in poolzy:
               gh.append(x)
          my_pool = gh[random.randint(0,len(gh)-1)]
          uden = my_pool["p_num"]
          depz = pools.find_one({"p_num":uden})
          depo = depz["player"]
          new_arr = depo + [b_id]
          pools.find_one_and_update({"p_num": uden}, {'$set': {"player": new_arr}})


     else:
          pool = pools.find({})
          for x in pool:
               gh.append(x)
          my_pool = gh[random.randint(0,len(gh) -1)]
          uden = my_pool["p_num"]
          depz = pools.find_one({"p_num":uden})
          depo = depz["player"]
          new_arr = depo + [b_id]
          pools.find_one_and_update({"p_num": uden}, {'$set': {"player": new_arr}})



     if request.method == "POST":
          dat = request.get_json()


     return render_template('pl3.html',mpl = names , mp = my_pool)






@application.route('/login/' , methods = ['POST','GET'])
@csrf.exempt
def login():
    if request.method == "POST":# and  hcaptcha.verify():
        email = request.form['email']
        existing_user  = users.find_one({'email':email} )
        if existing_user:
                passcode = request.form['passcode']
                v = str(existing_user['verified'])

                existing_pass = existing_user['password']
                if Hash_passcode.verify(passcode,existing_pass):
                    username = existing_user['email']
                    if username in session:
                        if v == '0' :
                             return redirect(url_for('complete_regist'))
                        else:
                            return redirect(url_for('feed'))
                    else:    
                        session.parmanent = True
                        session['login_user'] = email
                        return redirect(url_for('home'))
    return render_template('login.html')



@application.route('/logout/' , methods = ['POST','GET'])
@login_required
def logout():
    if request.method == "POST":
        if request.form['sub'] == "Yes":
            session.pop('login_user', None)
            return redirect(url_for('login'))
        else:
            return redirect(url_for('home'))
    return render_template('logout.html')

@application.route('/register/',methods = ['POST','GET'])
def register():

    if request.method == "POST":

#        pic = request.files['img']

        email = request.form['email']

#        username =  request.form['username']

        passc = request.form['passc']

        passc2 = request.form['passc2']

        hashed = Hash_passcode.hash(passc2)

        registered = users.find_one({"email":email})
        if registered:
            mess = "You are already registered,please Log in"
            return redirect(url_for('home'))
        if passc == passc2  and not registered:
          favs = []
          tags = []
          users.insert_one({"email":email  , "password":hashed ,"creator" : "no" , "verified" :0 ,
 'saved' : [], "viewed" :[] ,"posts" : 0  })

          if users.find_one({"email":email}):
                code = random.randint(145346 , 976578)
                code = str(code)
                session['login_user'] = email
                if not verif.find_one({"email" : email}):
                    verif.insert_one({"email" : email , "code" : code })
                    #send the code Here
                    send_mail(email,code)
                    return redirect(url_for('complete_regist'))
                else:
                    return redirect(url_for('complete_regist'))



    return render_template('register.html')


@application.route('/complete_regist' , methods = ['POST' , 'GET'])
def complete_regist():
    user_email = session['login_user']
    in_db = verif.find_one({"email" : user_email})
    if request.method == "POST":
        de_code = request.form['code']
        if in_db:
            code = str(in_db['code'])
            if code == de_code:
                users.find_one_and_update({"email" : user_email} ,{ '$set' :  {"verified": 1}} )
                verif.find_one_and_delete({'email' : user_email})
                return redirect(url_for('login'))
            else:
                print("Wrong Code")
                time.sleep(2)
                return redirect(url_for('complete_regist'))
        else:
            return redirect(url_for('register'))

    return render_template('verif_reg.html' , m = user_email)





if __name__ == '__main__':
    application.secret_key = "Fucddggdgdfdgdrer5677u"
    application.run(
        host='127.0.0.1',
        port=5006,
        debug=True
    )
