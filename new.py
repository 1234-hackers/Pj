

from flask import Flask, render_template, request, jsonify ,session, redirect,url_for

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


import passlib
from passlib.context import CryptContext
from passlib.hash import bcrypt_sha256,argon2,ldap_salted_md5,md5_crypt
import time
from datetime import  datetime as dt


from functools import wraps


from wtforms.csrf.session import SessionCSRF
from flask_wtf.csrf import CSRFProtect,CSRFError

import random
import requests

from pymongo import MongoClient
from pymongo.server_api import ServerApi


import secrets

uri = "mongodb+srv://jackson:mutamuta@hbcall.ihz6j.azure.mongodb.net/test?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

application = Flask(__name__)
Hash_passcode = CryptContext(schemes=["sha256_crypt" ,"des_crypt"],sha256_crypt__min_rounds=131072)
#mongo = PyMongo(application)

application.secret_key = "Fucddggdgdfdgdrer5677u"


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



@application.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    # Process the data as needed
    new_arr = []
    userz = session["login_user"]
    response = {'message': 'Form data received successfully!', 'data': data}
    gy = users.find_one({"email" : userz })
    num = int( response['data']['name'] )
    print(str(response )+"  " + userz + str(gy))
    """if not  gy["bets"] :
         new_arr = []
         new2 = new_arr + [num]
    else:
         new_arr = gy["bets"]
         new2 = new_arr + [num]
    print(new2)
    now = dt.now()
    now_c = now.strftime(" %Y:%m:%d ")
    timez = now_c
    if  not  userz  ==  " ":
         print("ryt"+ userz  + str(data) )
         de_user = users.find_one({"day": timez })
         users.find_one_and_update({"email": userz}, {'$set': {"bets": new2}})
    else:
         print("fvk")
     """
    return jsonify(response)




@application.route('/',methods = ["POST","GET"])
@login_required
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
          data = request.form.to_dict()
          # Process the data as needed
          response = {'message': 'Form data received successfully!', 'data': data}
          print(response)
          return jsonify(response)

     return render_template('pl3.html', mp = my_pool)

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
                            return redirect(url_for('home'))
                    else:
                        session['login_user'] = email
                        return redirect(url_for('home'))
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
        email = request.form['email']
        passc = request.form['passc']
        passc2 = request.form['passc2']

        hashed = Hash_passcode.hash(passc2)

        registered = users.find_one({"email":email})
        if registered:
            mess = "You are already registered,please Log in"
            return redirect(url_for('home'))
        if passc == passc2  and not registered:
          bets = []
          users.insert_one({"email":email  , "password":hashed ,"bets":bets, "verified" :0   })

          if users.find_one({"email":email}):
                code = random.randint(145346 , 976578)
                code = str(code)
                session['login_user'] = email
                if not verif.find_one({"email" : email}):
                    verif.insert_one({"email" : email , "code" : code })
                    #send the code Here
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
    me = session['login_user']
    fl = me[0:6] + "**"
    acc = users.find_one({"email" : me})
    bets = acc["bets"]

    return render_template('profile.html' , me = fl, bts = bets  )






if __name__ == '__main__':
    application.run(debug=True,port=5007)
