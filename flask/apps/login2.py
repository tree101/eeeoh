#!flask/bin/python
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
from flask.ext.sqlalchemy import SQLAlchemy

from urlparse import urlparse, urljoin
from flask.ext.wtf import Form
from flask.ext.bcrypt import Bcrypt

import psycopg2

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)

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
    ##  either renders the page for login info or if there is incoming it will check with the database and associate it 
    ## with a project. 
    pw_hash = bcrypt.generate_password_hash('fdfdseee')
    passornot = bcrypt.check_password_hash(pw_hash, 'boofdsfdk102') 
    if request.method == 'POST':
	# check username here.   
	#pw = request.form['password']
	#hashed = hashpw(pw, gensalt())
	#check = hashpw(pw, hashed)
        #session['username'] = hashed
        return redirect(url_for('index'))
    return render_template('login.html', hashed=passornot)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/db', methods=['GET', 'POST'])
def db_get():
    # remove the username from the session if it's there
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


### testing login flask 
@app.route('/login', methods=['GET', 'POST'])
def login2():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)	
# set the secret key.  keep this really secret:
app.secret_key = 'EEZr98j/*yX R~XHH!jmN]0)X/,?RT'
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)