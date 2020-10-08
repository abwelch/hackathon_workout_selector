import flask
import werkzeug
import mysql.connector
import os
from flask import render_template

#config and set up flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
	return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if flask.request.method == 'POST':
		# verify values submitted adhere to standards
		pass
	return render_template('register.html', error=error)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = None
	if flask.request.method == 'POST':
		# check values submitted against database
		pass
	return render_template('signin.html', error=error)


# run app
app.run()