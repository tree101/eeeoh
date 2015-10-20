#!flask/bin/python
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import escape


from urlparse import urlparse, urljoin
from flask.ext.wtf import Form

# password hash
from flask.ext.bcrypt import Bcrypt
# database access
import psycopg2
# login manager
from flask.ext.login import LoginManager

import re

app = Flask(__name__)
app.config.from_object('config')

# initiate hash 
bcrypt = Bcrypt(app)
#initiate login
lm = LoginManager()
lm.init_app(app)
# connect to postgres
conn = psycopg2.connect("dbname='eeeoh' user='alexsql' host='localhost' password='eeeoooh'")



@app.route('/')
def index():
    # check if user is login.  
    if 'username' in session:
		return render_template('index.html', name=escape(session['username']))
        #return 'Logged in as %s' % escape(session['username'])
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if its there is incoming password, then match password 
    if request.method == 'POST':
	pw = request.form['password']
	email = request.form['email']
	passornot = checkpassword(email,pw)
	if (passornot==0):
		return render_template('login.html')
	else:
		session['username'] = passornot
		return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/db', methods=['GET', 'POST'])
def db_get():
    # remove the username from the session if it's there
		index();
		cur = conn.cursor()
		#mydb = request.args.get("db")
		#SELECT * from action
		#SELECT * from action
		
		mydb = 'SELECT * from '+ 'userlogin'; 
		cur.execute(mydb)
		rows = cur.fetchall()
		out = '';
		for row in rows:
			#out = row[1]
			out = out+ '<tr>'+' '.join('<td>{0}</td>'.format(w) for w in row)+'</tr>'
	     
		#out = '<table>' + out + '</table>'
		#dbc = '<table></table>';
		return render_template('table.html',title='',table_stuff=out)
	


### make up stuff
def checkpassword(email,pw):
	# get user from database 
	# check if user even exists
	cur = conn.cursor()
	passornot = 0 
	mydb = 'Select * from userlogin where email=\''+email+'\' ';
	cur.execute(mydb)
	rows = cur.fetchall()
	if not rows:
		passornot = "user does not exists"
	else:
		name= rows[0][1] + " " + rows[0][2]
		group=rows[0][4]
		user=rows[0][3]
		# check 
		passornot = bcrypt.check_password_hash(rows[0][5], pw) 
		if(passornot==1):
			return name
		else:
			return 0
	
	
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)