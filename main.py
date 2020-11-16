from flask import Flask, request
from google.cloud import datastore
from google.oauth2 import id_token
from google.auth.transport import requests

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
def handle_validation():
	# TODO: Update to accept https requests
	# Verify user token; Check if existing Math Go user
	content = request.get_json()
	provided_gid = content.get("gid")
	provided_id_token = content.get("idToken")

	user_status = {}

	# Missing required fields = sign in fail
	if provided_gid == None or provided_id_token == None:
		print("Debug: Missing required field: gid or idToken")
		return "Missing required field: gid or idToken", 401

	# Verify user token
	valid_google_user = validate_google_user(provided_id_token);

	# Invalid user token
	if not valid_google_user:
		return "Invalid user token", 401

	# Check if provided_gid is an existing mathgo user datastore
	query = datastore_client.query(kind=constants.userEntity)
	query.add_filter('gid', '=', provided_gid)
	users = list(query.fetch())

	if (len(users) == 1) and (users[0]["gid"] == provided_gid):
		user_status["avatar"] = users[0]["avatar"]
		user_status["existingUser"] = True
	else:
		user_status["existingUser"] = False

	return json.dumps(user_status), 200


# Verify provided ID token with Google
def validate_google_user(provided_id_token):
	try:
		idinfo = id_token.verify_oauth2_token(provided_id_token, requests.Request(), "Enter_Google_Signin_webClientId")
	except ValueError:
		print("Debug: Issue validating user token")
		return False
	return True


@app.route('/user/registration', methods=['POST'])
def handle_registration():
	content = request.get_json()
	# grabs values from JSON sent from mobile application
	provided_gid = content.get("gid")
	provided_name = content.get("displayName")
	provided_avatar = content.get("avatar")

	# Error check required fields
	if provided_gid == None or provided_name == None or provided_avatar == None:
		logging.info("Debug: Missing required field(s): gid or name or avatar")
		return "Missing required field: gid, name, or avatar", 401

	# creating a new user to register into database
	new_user = datastore.entity.Entity(key=datastore_client.key(constants.userEntity))
	new_user.update({"displayName": provided_name, "gid": provided_gid, "avatar": provided_avatar})
	datastore_client.put(new_user)
	return "Added User Successfully", 201


@app.route('/math-problems', methods=['GET'])
def problemList():
	query = datastore_client.query(kind=constants.problemEntity)
	results = list(query.fetch())
	return json.dumps(results)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
