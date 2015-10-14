from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

## route to trigger function
## this function is called with the specific url
## each function has a specific url 
@app.route('/', methods=['GET', 'POST'])
def hello_world():
	name = request.args.get("user")
	return render_template('index.html', name=name)
	#return 'Hi world! %s ' % request.args.get("user")

## second page with function
## can pass it variables as well. 

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'hey dude %s' % username	
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)