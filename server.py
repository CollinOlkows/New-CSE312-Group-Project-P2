from flask import Flask,make_response,send_from_directory,render_template,request,redirect,url_for
import databaseutils
import bcrypt
import html
import secrets
import datetime


#File for all the server stuff

app = Flask(__name__)

@app.route('/<path:path>')
def send_static(path):
    response = make_response(send_from_directory('static', path),200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    return make_response('Home Page',200)

@app.route('/login')
def login():
    return make_response('Home Page',200)

@app.route('/signup')
def signup():
    return make_response('Home Page',200)

@app.route('/post')
def post():
    return make_response('Home Page',200)

@app.route('/feed')
def feed():
    return make_response('Home Page',200)


app.run(host='0.0.0.0',port=8080)