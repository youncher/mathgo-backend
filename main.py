from flask import Flask, request
from google.cloud import datastore

import constants
import json

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
datastore_client = datastore.Client()

@app.route('/')
def root():
    return 'Welcome to our CS467 capstone project! This serves as the backend (https://github.com/youncher/mathgo-backend) to our project, Math Go (https://github.com/youncher/mathgo).'

@app.route('/user/validation', methods=['POST'])
def user_validation():
	# Check if user is an existing Math Go user
	if request.method == 'POST':
		content = request.get_json()
		
		# TODO: Handle case if request body does not contain gid
		
		provided_gid = content["gid"]
		
		# Check if provided_gid is an existing mathgo user
		query = datastore_client.query(kind=constants.userEntity)
		query.add_filter('gid', '=', provided_gid)
		users = list(query.fetch())
		
		user_status = {}
		
		if (len(users) == 1) and (users[0]["gid"] == provided_gid):
			user_status["avatar"] = users[0]["avatar"]
			user_status["existingUser"] = True
		else:
			user_status["existingUser"] = False
			
		return json.dumps(user_status), 200
	else:
		return "Method not recognized"
	
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
