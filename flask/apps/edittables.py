#!flask/bin/python
from app import app
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
import pickle
from flask import jsonify
from urlparse import urlparse, urljoin
from flask.ext.wtf import Form

# password hash
from flask.ext.bcrypt import Bcrypt
# database access
import psycopg2
from psycopg2.extensions import AsIs
# login manager
from flask.ext.login import LoginManager
import json
import re
##################### my own rollups
from get import *



# initiate hash 
bcrypt = Bcrypt(app)

# connect to postgres
with open('./app/db.pickle') as f:
    pwd = pickle.load(f)
conn = psycopg2.connect(pwd[0])


##### creat forms here
@app.route('/edit_projects')
def edit_projects():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		
		return render_template("edit_projects.html",name=escape(session['username']))
    return redirect(url_for('login'))
