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
    token = request.cookies.get('auth',None)
    u = None
    login = False
    if token != None:
        u = databaseutils.get_user_by_token(token)
        login = True
    #check if users logged in, if yes show feed tab and username
    response = make_response(render_template('index.html',user=u,login=login),200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/login',methods=['POST', 'GET'])
def login():
    #check if users logged in, if yes redirect to feed
    login=False
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token)):
        response = make_response(redirect(url_for('index', _external=True)))
        response.set_cookie('auth',token)
        return response
    if request.method == 'GET':
        response = make_response(render_template('login.html',error='',login=login),200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        username = request.form.get('username',None)
        if username != None and username != '' and username != ' ':
            username = html.escape(username)
        else:
            response = make_response(render_template('login.html',error='Username Empty',login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        password = request.form.get('password')
        if(password == None or password==''):
            response = make_response(render_template('login.html',error='password empty',login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        user = databaseutils.get_user_by_username(username)
        if(user == None):
            response = make_response(render_template('login.html',error='No User Found',login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            ph=bcrypt.hashpw(password.encode(),user.salt)
            if ph==user.passhash:
                token = secrets.token_hex()
                databaseutils.set_user_token(username,token,datetime.datetime.now(tz=datetime.timezone.utc))
                response = make_response(redirect(url_for('index', _external=True)))
                response.set_cookie('auth',token)
                return response
            response = make_response(render_template('login.html',error='Password Incorrect',login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
                

@app.route('/signup',methods=['POST', 'GET'])
def signup():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token=token)):
        response = make_response(redirect(url_for('index', _external=True)))
        response.set_cookie('auth',token)
        return response
    #if users signed in redirect to home or feed
    if request.method == 'GET':
        response = make_response(render_template('signup.html',error='',login=login),200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        password_confirm = request.form.get('password_confirm',None)
        if(password!=password_confirm or password =='' or password == None):
            error = "Password empty or do not match"
            response = make_response(render_template('signup.html',error=error,login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        if(username==None or username=='' or username == ' '):
            error = "Username Field Empty"
            response = make_response(render_template('signup.html',error=error,login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        username=html.escape(username)
        error = ''
        test = databaseutils.add_user(username,password)
        if(test):
            #Set User Cookie Here
            token = secrets.token_hex()
            databaseutils.set_user_token(username,token,datetime.datetime.now(tz=datetime.timezone.utc))
            response = make_response(redirect(url_for('index', _external=True)))
            response.set_cookie('auth',token)
            return response
        else:
            error = "Username Already Exists"
            response = make_response(render_template('signup.html',error=error,login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
           
        #Check if the user can be create, if yes we login if no throw error

@app.route('/post')
def post():
    return make_response('Home Page',200)

@app.route('/feed')
def feed():
    return make_response('Home Page',200)


app.run(host='0.0.0.0',port=8080)