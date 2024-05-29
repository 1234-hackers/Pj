
import base64
from email import message
#from turtle import st
import shutil
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from dns.message import Message
from flask import Flask, render_template, url_for, request, redirect,flash,session
from flask.scaffold import F
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


def handle_csrf_error(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not f == "":
            return render_template('index.html', error=f), 400
        else:
            time.sleep(2)
            return redirect(url_for('home'))
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


@application.route('/',methods = ["POST","GET"])
def home():
     gh=[]
     b_id =  secrets.token_hex(13)
     bid = secrets.token_hex(12)
     dag = 5
     jmp = [bid]
     now = dt.now()
     now_c = now.strftime(" %Y:%m:%d ")
     timez = now_c
     result = []
     for num in range(1300, 1750 + 1):
          if num % 7 == 0 and num % 3 != 0 and num % 5 != 0:
               ks = result + [num*458]
     for num in range(1300, 1750 + 1):
          if num % 3 == 0 and num % 7 != 0 and num % 5 != 0:
               ks2 = ks + [num*458]

     for num in range(1300, 1750 + 1):
          if num % 5 == 0 and num % 3 != 0 and num % 7 != 0:
               k3 = ks2 + [num*458]

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


     return render_template('play2.html', mp = my_pool)

'''

     user_ip = request.remote_addr
     response = requests.get(f"https://ipinfo.io/{user_ip}")
     data = response.json()
     city = data.get('city', '')
     region = data.get('region', '')
     country = data.grt('country','')
     dag = ips.find_one({"ip":user_ip})

     if not dag:
          ips.insert_one({"city":city,"country":country,"ip":user_ip,"revisit":0})
     else:
          new_val = dag["revisit"] + 1
          ips.find_one_and_update({"ip" : user_ip} ,{ '$set' :  {"revisit": new_val}} )


     return render_template('play2.html', mp = my_pool)

'''

@application.route('/login/' , methods = ['POST','GET'])
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
                        return redirect(url_for('feed'))
    return render_template('login.html')


@application.route('/reset_pass/', methods = ['POST','GET'])
def  reset_pass():
    reset_db = client.flaka.pass_reset
    code = random.randint(145346 , 976578)
    code = str(code)
    if request.method == "POST":
        email = request.form['email']
        existing = users.find_one({'email':email} )
        if existing:

            '''
            Send message here with the co7de
            '''
            now = dt.now()
            r_now =  now.strftime("Date  %Y:%m:%d: Time %H:%M:%S")
            session['rset'] = email
            if not reset_db.find_one({"email" : email}):
                reset_db.insert_one({"email" : email , "code" : code , "time_in" : r_now})
            return redirect(url_for('enter_code'))      
        else:
            return redirect(url_for('register'))
    return render_template('reset_pass.html')


@application.route('/enter_code/' , methods = ['POST','GET'])
def enter_code():
    email = session['rset']
    if "x" =="x":
        if request.method == "POST":
            reset_db = client.flaka.pass_reset
            code = request.form['code']
            legit = reset_db.find_one({"email" : email})
            if legit:
                legit_code = legit["code"]
                now = dt.now()
                now = now.strftime("Date  %Y:%m:%d: Time %H:%M:%S")
                req_time = legit['time_in']
                def timez():
                    now = dt.now()
                    now3 = now.strftime("Date  %Y:%m:%d: Time %H:%M:%S")
                    cr = str(now3)[23:28]
                    first_min = cr[3:5]
                    first_hour = cr[0:2]

                    cr2 = str(req_time)[23:28]
                    second_min = cr2[3:5]
                    second_hour = cr2[0:2]

                    dif = int(second_min) - int(first_min)
                    hours = int(first_hour) - int(second_hour)
                    if dif < 0:
                        dif = dif + 60
                    return dif

                diff =timez()
                if code == legit_code:
                    reset_db.find_one_and_delete({'email' : email})
                    return redirect(url_for('peopleass'))  
                else:
                    return redirect(url_for('reset_pass' ))


    return render_template('enter_code.html')


def get_mpesa_token():

    consumer_key = "YOUR_APP_CONSUMER_KEY"
    consumer_secret = "YOUR_APP_CONSUMER_SECRET"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    return r.json()['access_token']


@application.route('/depositmpesa/' , methods = ['POST','GET'])
def depositmpesa():


     encode_data = b"<Business_shortcode><online_passkey><current timestamp>"
     passkey  = base64.b64encode(encode_data)
     try:
          access_token = get_mpesa_token()
          api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
          headers = { "Authorization": f"Bearer {access_token}" ,"Content-Type": "application/json" }
          data = MakeSTKPush.parser.parse_args()
          request = {
                "BusinessShortCode": "<business_shortCode>",
                "Password": str(passkey)[2:-1],
                "Timestamp": "<timeStamp>", # timestamp format: 20190317202903 yyyyMMhhmmss
                "TransactionType": "CustomerPayBillOnline",
                "Amount": data['amount'],
                "PartyA": data['phone'],
                "PartyB": "<business_shortCode>",
                "PhoneNumber": data['phone'],
                "CallBackURL": "<YOUR_CALLBACK_URL>",
                "AccountReference": "UNIQUE_REFERENCE",
                "TransactionDesc": ""
            }
          CheckoutRequestID = response.text['CheckoutRequestID']
          response = requests.post(api_url,json=request,headers=headers)
          if response.status_code > 299:
               return{
                    "success": False,
                    "message":"Sorry, something went wrong please try again later."
                },400

          return {
                "data": json.loads(response.text)
            },200

     except:
          return {
                "success":False,
                "message":"Sorry something went wrong please try again."
            },400
     return response


@application.route('/logout/' , methods = ['POST','GET'])
@login_required
def logout():
    if request.method == "POST":
        if request.form['sub'] == "Yes":
            session.pop('login_user', None)
            return redirect(url_for('login'))
        else:
            return redirect(url_for('feed')) 
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



@application.route('/profile/' , methods = ['POST','GET'])
@login_required
def profile():
    trend = client.flaka.trending
    me = session['login_user']
    me2 = me.replace("." , "")
    the_arr = ["electric car" , "rap" , "football"]
    acc = users.find_one({"email" : me})

    return render_template('profile.html' , me = me  )




if __name__ == "__main__":
    application.secret_key = "Fucddggdgdfdgdrer5677u"
    application.run(debug = True , port = 5006)
