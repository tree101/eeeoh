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


import psycopg2

app = Flask(__name__)
app.config.from_object('config')

conn = psycopg2.connect("dbname='alexsql' user='alexsql' host='localhost' password='eeeoooh'")

@app.route('/')
def index():
    if 'username' in session:
		return render_template('index.html', name=escape(session['username']))
        #return 'Logged in as %s' % escape(session['username'])
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
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
		cur = conn.cursor()
		mydb = request.args.get("db")
		#SELECT * from action
		#SELECT * from action
		
		mydb = 'SELECT * from '+ mydb; 
		cur.execute(mydb)
		rows = cur.fetchall()
		out = '';
		for row in rows:
			#out = row[1]
			out = out+ '<tr>'+' '.join('<td>{0}</td>'.format(w) for w in row)+'</tr>'
	     
		#out = '<table>' + out + '</table>'
		#dbc = '<table></table>';
		return render_template('table.html',title='',table_stuff=out)
	
# set the secret key.  keep this really secret:
app.secret_key = 'EEZr98j/*yX R~XHH!jmN]0)X/,?RT'
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)