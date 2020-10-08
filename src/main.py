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


@app.route('/register', methods=['GET'])
def register():
	return render_template('register.html', title='Register')


@app.route('/signin', methods=['GET'])
def signin():
	return render_template('signin.html', title='Sign In')


# run app
app.run()