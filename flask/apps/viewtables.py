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
from datetime import datetime
##################### my own rollups
from get import *



# initiate hash 
bcrypt = Bcrypt(app)

# connect to postgres
with open('./app/db.pickle') as f:
    pwd = pickle.load(f)
conn = psycopg2.connect(pwd[0])


##### viewing tables ok
@app.route('/table_user')
def table_user():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		cur = conn.cursor()
		admin = checkuser(cur, session['username'])
		if (admin != 1):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		numrowstart = int(request.args.get('numrows'))
		numrowend = numrowstart+ 50
		head = ['name','email','notes','user type','name of project']
		
		c = 'SELECT userlogin.firstname, userlogin.email, userlogin.notes, userlogin_projects.usertype, projects.name FROM userlogin INNER JOIN userlogin_projects ON userlogin.id = userlogin_projects.userlogin_id INNER JOIN projects ON userlogin_projects.project_id = projects.id LIMIT %s OFFSET %s;';
		cur.execute(c, (numrowend,numrowstart)) 
		rows = cur.fetchall()
		#rows.append(head)
		rows.insert(0,head)

		return render_template("table_view.html",data=rows,name=escape(session['username']))
    return redirect(url_for('login'))


@app.route('/table_projects', methods=['GET', 'POST'])
def table_projects():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		cur = conn.cursor()
		admin = checkuser(cur, session['username'])
		if (admin != 1):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		# now check if this is view only or add record then view 
		action = int(request.args.get('action'))
		# add record if action ==1 
		# add record if action == -1
		dt = datetime.now()
		whatdidyoudo = 0
		## adding record 
		if action == 1:
			
			name_project =  request.args.get('name')
			group_name   =  request.args.get('groupname')
			notes =         request.args.get('notes')
			cInsert = ('INSERT INTO projects (name, groupname, notes) VALUES (%s, %s,%s);')
			cur.execute(cInsert, (name_project,group_name,notes))
			conn.commit()
			whatdidyoudo = "%s just inserted %s %s into table projects" % (session['username'],name_project,group_name) 
		# delete here instead
		if action == -1:
			id = request.args.get('id')
			delete_this = 'DELETE FROM projects WHERE id = %s;';
			cur.execute(delete_this, (id,)) 
			conn.commit()
			whatdidyoudo = "%s just deleted id %s from table projects " % (session['username'],id) 
		
		# now that all the action is completed - lets store it into the logger
		if whatdidyoudo != 0:  
			logc = 'INSERT INTO logger (tablename, username,timestamp,lognotes) VALUES (\'projects\',%s,DEFAULT,%s);'
			cur.execute(logc, (session['username'],whatdidyoudo)) 
			conn.commit()
		# end logger
		# get limits, currently limiting 50 per search
		numrowstart = int(request.args.get('numrows'))
		numrowend = numrowstart+ 50
		head = ['ID','Name','Group Name','Notes','Delete']
		
		c = 'SELECT id, name, groupname,notes FROM projects LIMIT %s OFFSET %s;';
		cur.execute(c, (numrowend,numrowstart)) 
		rows = cur.fetchall()
		#rows.append(head)
		#rows.insert(0,head)
		# lets not do the above; its easier but to stringent, instead pass header info as a seperate var

		return render_template("table_view.html",data=rows,name=escape(session['username']),headinfo= head, whatdidyoudo=whatdidyoudo,route='table_projects')
    return redirect(url_for('login'))


@app.route('/table_location', methods=['GET', 'POST'])
def table_location():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		cur = conn.cursor()
		admin = checkuser(cur, session['username'])
		# not sure if this needs to be an admin account
		# change back to 1 if you want admin access only 
		whatdidyoudo = 0 # setting this to 0 is important to produce an additiona link to render children view
		if (admin == 100):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		# now check if this is view only or add record then view 
		action = int(request.args.get('action'))
		try:
			parent_id = int(request.args.get('parent_id'))
		except:
			pass
		
		
		
		# add record if action ==1 
		# add record if action == -1
		if action == 1: 
			parent_record = request.args.get('pname')
			parent_id2 = parent_record.split(",")
			nname = request.args.get('nname')
			notes = request.args.get('notes')
			clocation = 'INSERT INTO location (parent_id, name,notes) VALUES (%s,%s,%s);'
			cur.execute(clocation,(parent_id2[0],nname,notes))
			conn.commit() 
			# see child instead
			parent_id = int(parent_id2[0])
			whatdidyoudo = "%s Inserted a new record into location form = %s notes = %s" % (session['username'], nname,notes )
			# return 
		
		if action == -1:
			return render_template("error.html",error="Sorry at this moment deleting from storage is not allow",name=escape(session['username'])   )
			
		
		if action != 0:  
			logc = 'INSERT INTO logger (tablename, username,timestamp,lognotes) VALUES (\'location\',%s,DEFAULT,%s);'
			cur.execute(logc, (session['username'],whatdidyoudo)) 
			conn.commit()
		
		head = ['id','parent','name','notes','delete','more']
		if (parent_id  == 0):
			c = 'SELECT id, parent_id, name, notes FROM location WHERE parent_id is NULL ; ';
			cur.execute(c)
		else:
			c = 'SELECT id, parent_id, name, notes FROM location WHERE parent_id = %s ; ';
			cur.execute(c,(parent_id, )) 
		
		rows = cur.fetchall()
		

		return render_template("table_view.html",data=rows,name=escape(session['username']),headinfo= head, whatdidyoudo=0,route='table_location',location=1, back=0)
    return redirect(url_for('login'))
    

@app.route('/table_diagnosis', methods=['GET', 'POST'])
def table_diagnosis():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		cur = conn.cursor()
		admin = checkuser(cur, session['username'])
		# not sure if this needs to be an admin account
		# change back to 1 if you want admin access only 
		whatdidyoudo = 0
		if (admin == 100):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		# now check if this is view only or add record then view 
		action = int(request.args.get('action'))
		
		# add record if action ==1 
		# add record if action == -1
		if action == 1: 
			diagnosis = request.args.get('diagnosis_name')
			
			notes = request.args.get('notes')
			cdiagnosis = 'INSERT INTO diagnosis (disease,notes) VALUES (%s,%s);'
			cur.execute(cdiagnosis,(diagnosis,notes))
			conn.commit() 
			whatdidyoudo = "%s Inserted a new record into diagnosis form = %s notes = %s" % (session['username'], diagnosis,notes )
		
		if action == -1:
			id = request.args.get('id')
			delete_this = 'DELETE FROM diagnosis WHERE id = %s;';
			cur.execute(delete_this, (id,)) 
			conn.commit()
			whatdidyoudo = "%s just deleted id %s from table diagnosis " % (session['username'],id)
		
		if action != 0:  
			logc = 'INSERT INTO logger (tablename, username,timestamp,lognotes) VALUES (\'diagnosis\',%s,DEFAULT,%s);'
			cur.execute(logc, (session['username'],whatdidyoudo)) 
			conn.commit()
		
		numrowstart = int(request.args.get('numrows'))
		numrowend = numrowstart+ 50
		head = ['id','disease','notes','delete']
		
		c = 'SELECT id, disease, notes FROM diagnosis LIMIT %s OFFSET %s;';
		cur.execute(c, (numrowend,numrowstart)) 
		
		rows = cur.fetchall()
		

		return render_template("table_view.html",data=rows,name=escape(session['username']),headinfo= head, whatdidyoudo=whatdidyoudo,route='table_diagnosis')
    return redirect(url_for('login'))


@app.route('/table_consent', methods=['GET', 'POST'])
def table_consent():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		cur = conn.cursor()
		admin = checkuser(cur, session['username'])
		# not sure if this needs to be an admin account
		# change back to 1 if you want admin access only 
		if (admin == 100):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		# now check if this is view only or add record then view 
		action = int(request.args.get('action'))
		whatdidyoudo = 0 # important to set to 0 otherwise it will log this activity
		# add record if action ==1 
		# add record if action == -1
		if action == 1: 
			consent = request.args.get('consent_name')
			notes = request.args.get('notes')
			cconsent = 'INSERT INTO consent (form,notes) VALUES (%s,%s);'
			cur.execute(cconsent,(consent,notes))
			conn.commit()
			whatdidyoudo = "%s Inserted a new record into consent form = %s notes = %s" % (session['username'], consent,notes ) 
		if action == -1:
			id = request.args.get('id')
			delete_this = 'DELETE FROM consent WHERE id = %s;';
			cur.execute(delete_this, (id,)) 
			conn.commit()
			whatdidyoudo = "%s just deleted id %s from table consent " % (session['username'],id)
			 
		# now that all the action is completed - lets store it into the logger
		if action != 0:  
			logc = 'INSERT INTO logger (tablename, username,timestamp,lognotes) VALUES (\'consent\',%s,DEFAULT,%s);'
			cur.execute(logc, (session['username'],whatdidyoudo)) 
			conn.commit()
		
		numrowstart = int(request.args.get('numrows'))
		numrowend = numrowstart+ 50
		head = ['id','form','links','notes','delete']
		
		c = 'SELECT id, form, link, notes FROM consent LIMIT %s OFFSET %s;';
		cur.execute(c, (numrowend,numrowstart)) 
		
		rows = cur.fetchall()
		

		return render_template("table_view.html",data=rows,name=escape(session['username']),headinfo= head, whatdidyoudo=whatdidyoudo,route='table_consent')
    return redirect(url_for('login'))
    



@app.route('/table_logger', methods=['GET', 'POST'])
def table_logger():
    # check if user is login.  
    if 'username' in session:
		# needs to check if user is administrator here. 
		cur = conn.cursor()
		admin = checkuser(cur, session['username'])
		if (admin != 1):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		# now check if this is view only or add record then view 
		action = int(request.args.get('action'))
		
		if action == -1:
			return render_template("error.html",error="Sorry at this moment deleting from logger is not allow",name=escape(session['username'])   )
		
		# get limits, currently limiting 50 per search
		numrowstart = int(request.args.get('numrows'))
		numrowend = numrowstart+ 50
		head = ['Table Name', 'Who did this', 'When', 'Action','delete']
		c = 'SELECT tablename, username, timestamp, lognotes FROM logger LIMIT %s OFFSET %s;';
		cur.execute(c, (numrowend,numrowstart)) 
		rows = cur.fetchall()
		#rows.append(head)
		#rows.insert(0,head)
		# lets not do the above; its easier but to stringent, instead pass header info as a seperate var

		return render_template("table_view.html",data=rows,name=escape(session['username']),headinfo= head, whatdidyoudo='viewing log',route='table_logger')
    return redirect(url_for('login'))
    

@app.route('/table_test')
def table_test():
    # check if user is login.  
    if 'username' in session:
		cur = conn.cursor()
		numrowstart = int(request.args.get('numrows'))
		numrowend = numrowstart+ 50
		head = ['name','email','notes','user type','name of project']
		selectThis = " userlogin.firstname, userlogin.email, userlogin.notes, userlogin_projects.usertype, projects.name "
		c = 'SELECT %(selectThis)s FROM userlogin INNER JOIN userlogin_projects ON userlogin.id = userlogin_projects.userlogin_id INNER JOIN projects ON userlogin_projects.project_id = projects.id ;';
		cur.execute(c, {"selectThis": AsIs(selectThis)}) 
		
		rows = cur.fetchall()
		#rows.append(head)
		rows.insert(0,head)

		return render_template("table_view.html",data=rows,name=escape(session['username']))
    return redirect(url_for('login'))
	

