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

# run app
app.run()