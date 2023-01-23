from flask import *
from flask_login import *
import os
import re
import datetime

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey


app = Flask(__name__)
app.secret_key = "askubusku"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader():
    return

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


@app.route('/login')
def login():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)