#!/usr/bin/python3.8

import flask
import Flask-JWT
import werkzeug
import mysql.connector
import os

#config and set up flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

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
cnx = mysql.connector.connect(**config)

#### Helper Functions ####



### App Routes ####

@app.route('/signup', methods=['POST'])
def register():
	error = None
	if flask.request.method == 'POST':
		# verify values submitted adhere to standards
		pass
	return render_template('register.html', error=error)


# run app
app.run()
