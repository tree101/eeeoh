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
		if (admin == 100):
			return render_template("error.html",error="you need to be a amdiminstrator to access this",name=escape(session['username'])   )
		# now check if this is view only or add record then view 
		action = int(request.args.get('action'))
		# add record if action ==1 
		# add record if action == -1
		
		whatdidyoudo = 0
		parent_id = int(request.args.get('parent_id'))
		head = ['id','name','rows','cols','notes','delete','more']
		if (parent_id  == 0):
			c = 'SELECT id parent_id, name, rows, cols, notes FROM location WHERE parent_id is NULL ; ';
			cur.execute(c)
		else:
			c = 'SELECT id parent_id, name, rows, cols, notes FROM location WHERE parent_id = %s ; ';
			cur.execute(c,(parent_id, )) 
		
		rows = cur.fetchall()
		

		return render_template("table_view.html",data=rows,name=escape(session['username']),headinfo= head, whatdidyoudo=whatdidyoudo,route='table_location',location=1, back=0)
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
	

