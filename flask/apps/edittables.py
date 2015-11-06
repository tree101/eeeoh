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
import uuid
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
		
		
		return render_template("edit_sampletype.html",name=escape(session['username']),isearch=rows)
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



@app.route('/edit_sample')
def edit_sample():
    # check if user is login.  
    if 'username' in session:
		cur = conn.cursor()
		
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		ajDothis = request.args.get('ajDothis', type=int)
		# do the ajax first 
		# lets get uuid for all subject and samples
		if ajDothis == 0:
			c = 'SELECT id, age, sex, COALESCE(to_char(date_collection, \'MM-DD-YYYY\'), \'\') AS date_collection FROM subject';
			cur.execute(c) 
			srows = cur.fetchall()
			# now get sample type
			csampletype= 'SELECT id, tissue, cat FROM sampletype';
			cur.execute(csampletype)
			strows = cur.fetchall()
			# get subtypes
			csubtype= 'SELECT id, subtype FROM subtype';
			cur.execute(csubtype)
			subrows = cur.fetchall()
			
			# get units
			cunit= 'SELECT unit FROM unit';
			cur.execute(cunit)
			unitrows = cur.fetchall()
			
			# get list of locations
			# first get mother nodes, usually institutions but you never ever know, hee hee
			lc = 'SELECT id, name FROM location WHERE parent_id IS NULL;'
			cur.execute(lc)
			lcrows = cur.fetchall()
			location = []
			for l in lcrows:
				locationt=getChild_location(cur,l[0],l[1],[])
				location.append(locationt)
			return render_template("edit_sample.html",name=escape(session['username']), IDs=srows, sampletype=strows, subtype=subrows, location=location, unit=unitrows )
		
		
		
		
		
    return redirect(url_for('login'))




@app.route('/edit_sample2')
def edit_sample2():
    # check if user is login.  
    if 'username' in session:
		cur = conn.cursor()
		
		# needs to check if user is administrator here. 
		# open connection to projects and populate this for instant searching
		ajDothis = request.args.get('ajDothis', type=int)
		if (ajDothis ==1):
			xtable = request.args.get('xtable')
			id = xtable.split(",")
			if id:
				srows=[]
				try:
					c = 'SELECT id, sampletype_id, subtype_id, COALESCE(to_char(date_collection, \'MM-DD-YYYY\'), \'\') AS date_collection from sample where subject_id = %s';
					cur.execute(c, (id[0],)) 
					srows = cur.fetchall()
				except:
					conn.rollback()
				return jsonify(result=srows)
		if (ajDothis ==2):
			subject = request.args.get('subject')
			id = subject.split(",")
			# main fields
			subject = id[0]
			datec = request.args.get('datec')
			sample_id = request.args.getlist('sample_id')
			# will need to split samples up
			sample_type = request.args.get('sample_type')
			sample_subtype = request.args.get('sample_subtype')
			location = request.args.get('location')
			location = location.split(",")
			addloc= request.args.get('addloc')
			# check if addloc has anything 
			weight= request.args.get('weight')
			# new entry also needs to consider remaining set to weight
			remaining = weight
            
			tissue_unit= request.args.get('tissue_unit')
			accession= request.args.get('accession')
			percent_tumor= request.args.get('percent_tumor')
			state= request.args.get('state')
			stage= request.args.get('stage')
			label= request.args.get('label')
			notes= request.args.get('notes')
			
			new_sample_id = str(uuid.uuid4());
			# prepare JSON stuff for samples
			meta = ('{'
					'"accession":"%s",'
					'"percent_tumor":"%s",'
					'"state":"%s",'
					'"stage":"%s",'
					'"i_weight":"%s",'
					'"i_remaining":"%s",'
					'"unit":"%s",'
					'"label":"%s"'

			'}') % (accession,percent_tumor,state,stage,weight,remaining,tissue_unit,label)
			
			# need to get file upload right here
			# ok lets try some insertion here
			insertc = (' INSERT INTO sample '
					   '(id, subject_id, sampletype_id, subtype_id,timestamp,'
					   ' date_collection, users,'
					   'location_id,label,parent,notes,meta) '
					   ' VALUES (%s,%s,%s,%s,DEFAULT,%s,%s,%s,%s,%s,%s,%s);'
					   )
			# also needs one for the join table
			# ignore for now ok?
			# lets do some insertion here

			# we need to consider adding to the joint table now
			jointc = ''
			child = new_sample_id;
			parent = new_sample_id;

			if int(sample_id[0]) == -1:
				# then child and parent are the same
				child = new_sample_id;
				parent = new_sample_id;

			
			try:
				cur.execute(insertc, (new_sample_id,subject,sample_type,sample_subtype,datec,session['username'],location[0],label,parent,notes,meta)) 
				conn.commit()
				jointc = 'good'
			except:
				conn.rollback()
				jointc = 'no good'
			return jsonify(result=[new_sample_id,sample_type,sample_subtype,sample_id[0],jointc])
		
		
		
		
    return redirect(url_for('login'))
