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
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		c = 'SELECT id, name,notes FROM projects';
		cur.execute(c) 
		rows = cur.fetchall()
		c = 'SELECT DISTINCT groupname FROM projects';
		cur.execute(c)
		rows2 = cur.fetchall()
		return render_template("edit_projects.html",name=escape(session['username']),isearch=rows,isearch2=rows2)
    return redirect(url_for('login'))


##### creat forms here
@app.route('/edit_location')
def edit_location():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		c = 'SELECT id, name, notes FROM location';
		cur.execute(c) 
		rows = cur.fetchall()
		
		return render_template("edit_locations.html",name=escape(session['username']),isearch=rows)
    return redirect(url_for('login'))

@app.route('/edit_diagnosis')
def edit_diagnosis():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		c = 'SELECT disease FROM diagnosis';
		cur.execute(c) 
		rows = cur.fetchall()
		
		return render_template("edit_diagnosis.html",name=escape(session['username']),isearch=rows)
    return redirect(url_for('login'))


@app.route('/edit_consent')
def edit_consent():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		c = 'SELECT form FROM consent';
		cur.execute(c) 
		rows = cur.fetchall()
		
		return render_template("edit_consent.html",name=escape(session['username']),isearch=rows)
    return redirect(url_for('login'))


@app.route('/edit_subtype')
def edit_subtype():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		c = 'SELECT subtype FROM subtype';
		cur.execute(c) 
		rows = cur.fetchall()
		
		return render_template("edit_subtype.html",name=escape(session['username']),isearch=rows)
    return redirect(url_for('login'))


# c = 'SELECT sampletype.id, sampletype.tissue, subtype.subtype, sampletype.notes FROM sampletype INNER JOIN subtype ON sampletype.subtype_id = subtype.id LIMIT %s OFFSET %s;';

@app.route('/edit_sampletype')
def edit_sampletype():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		c = 'SELECT DISTINCT sampletype.tissue FROM sampletype';
		cur.execute(c) 
		rows = cur.fetchall()
		
		c = 'SELECT id,subtype FROM subtype';
		cur.execute(c) 
		rows2 = cur.fetchall()
		
		return render_template("edit_sampletype.html",name=escape(session['username']),isearch=rows,isearch2=rows2)
    return redirect(url_for('login'))

@app.route('/edit_subject')
def edit_subject():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		cur = conn.cursor()
		# get consents 
		c = 'SELECT id, form FROM consent';
		cur.execute(c) 
		crows = cur.fetchall()
		# get projects
		c = 'SELECT id, name FROM projects';
		cur.execute(c) 
		prows = cur.fetchall()
		# get 
		c = 'SELECT id, disease FROM diagnosis';
		cur.execute(c) 
		drows = cur.fetchall()
		
		return render_template("edit_subject.html",name=escape(session['username']),consentSearch=crows,projectSearch=prows,diagnosisSearch=drows)
    return redirect(url_for('login'))
