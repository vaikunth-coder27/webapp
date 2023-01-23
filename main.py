from flask import *
from flask_login import *
import os
import re
import datetime

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from flask import Flask, app, render_template, request
from PIL import Image

app = Flask(_name_)
app.secret_key = "askubusku"
login_manager = LoginManager()
login_manager.init_app(app)

client = Cloudant.iam(
    'e3c83642-37dd-4e55-b2c0-ed508ffa632b-bluemix','yUJHiAM1KxNb--4tW0DeOhpOvnu2OYoR_oGGD3GZHpdC',connect=True)
name = 'name'
email = 'a@b.c'
password = '123'

user_database = client.create_database('user_database')
#user_image_database = client.create_database('user_image_database')



def database_updation(name,email,password):
    global user_database
    jsonDocument = {
	'_id':email.replace('@','').replace('.',''),
        'name':name,
        'email':email,
        'password':password
    }
    newDocument = user_database.create_document(jsonDocument)
    if(newDocument.exists()):
        print('database updated')
    else:
        print('database couldn\'t be edited')
    return


def database_retrieval():
    global user_database
    result_retrieved = Result(user_database.all_docs,include_docs=True)
    #print(list(result_retrieved))
    result = {}
    for i in list(result_retrieved):
        result[i['doc']['email']]={'name':i['doc']['name'],'password':i['doc']['password']}
    return result
#print(database_retrieval())


user = {'a@b.c': {'password': '123'}}


@login_manager.user_loader
def user_loader():
    data=database_retrieval()
    if email not in data:
        return 
    user=User()
    user.id=email
    user.name = data[email]['name']
    
    return user


@login_manager.request_loader
def request_loader(a=1):
    if(a):
        w=1
    else:
        w=0
    return 



@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login',methods =['GET','POST'])
def login():
    data = database_retrieval()
    if(request.method == 'GET'):
        
        return render_template('login.html',flash_message='False')
    email = request.form['email']
    if(email in data and request.form['password']==data[email]['password']):
       
        return render_template('homepage.html',flash_message='Fal')
    #flask.flash('invalid credentials !!!')
    return render_template('login.html',flash_message="True")
    

@app.route('/register',methods = ['GET','POST'])
def register():
    data = database_retrieval()
    if(request.method == 'GET'):
        return render_template('register.html')
    email = request.form['email']

    database_updation(request.form['name'],request.form['email'],request.form['password'])
        #users[email]={'password':flask.request.form['password']}
    
    return render_template('register.html')

if _name=='__main_':
    app.run(debug=True)
