#!/usr/bin/python3.8

import flask
import flask_jwt_extended
import werkzeug
import mysql.connector
import os
import json

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

def retrieve_all_workouts():
	cursor = cnx.cursor()

	query = "select * from workout_plans;"
	cursor.execute(query)
	plans = cursor.fetchall()

	query = "select * from exercises;"
	cursor.execute(query)
	exercises = cursor.fetchall()

	# this needs to be altered to properly nest array of jsons for the exercises within each workout
	# current version will create entirely new workout json for each exercise related to a workout
	# works fine for now since functionlity does not exist to add more than one exercise to a workout
	full_workout = []
	for plan_row in plans:
		for ex_row in exercises:
			if plan_row[0] == ex_row[5]:
				entry = {
					"upvotes": plan_row[1], 
					"workout_title": plan_row[2], 
					"workout_desc": plan_row[3], 
					"exercise_title": ex_row[1], 
					"exercise_desc": ex_row[2], 
					"sets": ex_row[3], 
					"reps": ex_row[4]
				}
				full_workout.append(entry)
	return json.dumps(full_workout)


def add_workout_plan(userID, workout_title, workout_descr, exercise_title, exercise_descr, exercise_reps, exercise_sets):
	cursor = cnx.cursor()

	query = """
			INSERT INTO workout_plans (upvotes, title, descr, total_exercises, creatorID)
			VALUES ('{}', '{}', '{}', '{}', '{}')
			""".format(1, workout_title, workout_descr, 1, userID)
	cursor.execute(query)
	cnx.commit()

	# retrieve auto_incremented key for workout plan
	workoutID = cursor.lastrowid
	query = """
			INSERT INTO exercises (title, descr, sets, reps, workoutID) 
			VALUES ('{}', '{}', '{}', '{}', '{}')
			""".format(exercise_title, exercise_descr, exercise_sets, exercise_reps, workoutID)
	cursor.execute(query)
	cnx.commit()

	cursor.close()


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
		flask.abort(411, description=uname)

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


@app.route('/create_workout', methods=['POST'])
def create_workout():
	# get the json data from the request
	try:
		json_data = flask.request.json
	except Exception as e:
		flask.abort(400, description="Did not include all fields")
	
	# make sure the JSON has all required fields, if not abort and return error
	if ( "userID" not in json_data ) or ( "workout_title" not in json_data ) or ( "workout_descr" not in json_data ) or ( "exercise_title" not in json_data ) or ( "exercise_descr" not in json_data ) or ( "exercise_sets" not in json_data ) or ( "exercise_reps" not in json_data ):
		flask.abort(402, description="Did not include all fields")

	# extract info
	userID = json_data["userID"]
	workout_title = json_data["workout_title"]
	workout_descr = json_data["workout_descr"]
	exercise_title = json_data["exercise_title"]
	exercise_descr = json_data["exercise_descr"]
	exercise_sets = json_data["exercise_sets"]
	exercise_reps = json_data["exercise_reps"]
	print(json_data)

	add_workout_plan(userID, workout_title, workout_descr, exercise_title, exercise_descr, exercise_reps, exercise_sets)

	return flask.jsonify(success=True)


@app.route('/retrieve_workouts', methods=["GET"])
def retrieve_workouts():
	return retrieve_all_workouts()

# run app
app.run()
