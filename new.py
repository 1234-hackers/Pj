

from flask import Flask, render_template, request, jsonify

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

import random
import requests

from pymongo import MongoClient
from pymongo.server_api import ServerApi


import secrets

uri = "mongodb+srv://jackson:mutamuta@hbcall.ihz6j.azure.mongodb.net/test?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


application = Flask(__name__)

#csrf = CSRFProtect(application)

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







@application.route('/')
def index():
    return render_template('indexy.html')




@application.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    # Process the data as needed
    response = {'message': 'Form data received successfully!', 'data': data}
    num = int( response['data']['name'] )
    print(num)
    if data :
         print("ryt" + str(data) )
    else:
         print("fvk")

    return jsonify(response)




@application.route('/p',methods = ["POST","GET"])
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






if __name__ == '__main__':
    application.run(debug=True,port=5007)
