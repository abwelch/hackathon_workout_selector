#!/usr/bin/python3.8

import flask
import flask_jwt_extended
import werkzeug
import mysql.connector
import os

#config and set up flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# config JWT for the app

app.config['JWT_SECRET_KEY'] = 'root'
jwt = flask_jwt_extended.JWTManager(app)

# get env vars for DB connections

mysql_root_password = os.environ['MYSQL_ROOT_PASSWORD']
mysql_user = os.environ['MYSQL_USER']
mysql_host = os.environ['MYSQL_HOST']
mysql_db = os.environ['MYSQL_DB']

# configure the mysql conn
mysql_config = {
	'user': mysql_user,
	'password': mysql_root_password,
	'host': mysql_host,
	'database': mysql_db
}

# connect to sql
cnx = mysql.connector.connect(**mysql_config)

#### Helper Functions ####


# check to see if the user already exists
def user_already_exists(username:str) -> bool:
	cursor = cnx.cursor()

	query = "SELECT * FROM users WHERE username = '{}'".format(username)
	
	cursor.execute(query)
	r = cursor.fetchone()

	cursor.close()

	if r == None:
		return False # the user does not exist already
	else:
		return True # the user exists already

# add the user to the database
def add_user(username:str, password:str, email:str) -> None:
	
	cursor = cnx.cursor()

	query = "INSERT INTO users (username, password, email) VALUES ('{}', '{}', '{}')".format(username, password, email)

	cursor.execute(query)
	cnx.commit()

	cursor.close()

	return None

# see if user credentials match
def verify_credentials(username, password):
	cursor = cnx.cursor()

	query = "SELECT * FROM users WHERE username = '{}' and password = '{}'".format(username, password)

	cursor.execute(query)
	r = cursor.fetchone()

	cursor.close()

	if r == None:
		return False # invalid credentials
	else:
		return True # valid credentials

### Error Handling ####

@app.errorhandler(400)
def missing_data(e):
	return flask.jsonify(error=str(e)), 400

@app.errorhandler(409)
def user_already_exists(e):
	return flask.jsonify(error=str(e)), 409

### App Routes ####

@app.route('/signup', methods=['POST'])
def sign_up():
	# get the json data from the request
	try:
		json_data = flask.request.json
	except Exception as e:
		flask.abort(400, description="Did not include all fields")

	# make sure the JSON has all required fields, if not abort and return error
	if ( "username" not in json_data ) or ( "password" not in json_data ) or ( "email" not in json_data ):
		flask.abort(400, description="Did not include all fields")

	# extract the information from JSON
	uname = json_data["username"]
	pword = json_data["password"]
	email = json_data["email"]

	if ( user_already_exists(uname) ):
		# see if user exists. If they do return error. Username is identifying unique data for our schema, so everyone must have a globally unique username
		flask.abort(409, description="User already exists")

	else:
		# If the user does not already exist, sign the new user up and return success.
		add_user(uname, pword, email)
		resp = flask.jsonify(success=True)

		return resp

@app.route('/signin', methods=['GET'])
def sign_in():
	# get the json data from request
	try: 
		json_data = flask.request.json
	except Exception as e:
		flask.abort(400, description="Did not include all fields")

	# make sure the data provided contains everythin
	if ( "username" not in json_data ) or ( "password" not in json_data ):
		flask.abort(400, description="Did not include all fields")

	# extract the info
	uname = json_data["username"]
	pword = json_data["password"]

	# attempt to log in
	if ( verify_credentials(uname, pword) ):
		access_token = flask_jwt_extended.create_access_token(identity=uname)
		return flask.jsonify(access_token=access_token), 200
	else:
		return flask.jsonify({"msg":"Bad username or password"}), 401
		

@app.route('/protected', methods=['GET'])
@flask_jwt_extended.jwt_required
def protected():
	curr_user = flask_jwt_extended.get_jwt_identity()
	return flask.jsonify(logged_in_as=curr_user), 200

# run app
app.run()
