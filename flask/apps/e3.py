from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import escape

app = Flask(__name__)

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

# set the secret key.  keep this really secret:
app.secret_key = 'EEZr98j/*yX R~XHH!jmN]0)X/,?RT'
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)