from flask import Flask,make_response,send_from_directory,render_template,request,redirect,url_for
import databaseutils
import bcrypt
import html
import secrets
import json
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
    if(token !=None and databaseutils.check_token(token)):
        response = make_response(redirect(url_for('feed', _external=True)))
        return response
    else:
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
        response = make_response(redirect(url_for('feed', _external=True)))
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
                databaseutils.set_user_token(username,token,datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                response = make_response(redirect(url_for('index', _external=True)))
                response.set_cookie('auth',token,max_age=3600,httponly=True)
                return response
            response = make_response(render_template('login.html',error='Password Incorrect',login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
                

@app.route('/signup',methods=['POST', 'GET'])
def signup():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token=token)):
        response = make_response(redirect(url_for('feed', _external=True)))
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
            databaseutils.set_user_token(username,token,datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            response = make_response(redirect(url_for('feed', _external=True)))
            response.set_cookie('auth',token,max_age=3600,httponly=True)
            return response
        else:
            error = "Username Already Exists"
            response = make_response(render_template('signup.html',error=error,login=login),200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
           
        #Check if the user can be create, if yes we login if no throw error


@app.route('/feed')
def feed():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token=token)):
        posts = databaseutils.get_all_posts()
        user = databaseutils.get_user_by_token(token=token)
        response = make_response(render_template('feed.html',posts=posts,user=user,time=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),login=True),200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect(url_for('login')))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/post',methods=['POST', 'GET'])
def post():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token)):
        if request.method== "POST":
            print('hello')
            content = html.escape(request.json['content'])
            title = html.escape(request.json['title'])
            user = databaseutils.get_user_by_token(token)
            databaseutils.add_post(user,content,title)
            print('hello')
            return make_response('Post Successful!',200)
        else:
            response = make_response(redirect(url_for('feed')))
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
    else:
        response = make_response(redirect(url_for('login')))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/like_post',methods=['POST'])
def like_post():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token)):
        user = databaseutils.get_user_by_token(token=token)
        post_id = html.escape(request.json['post_id'])
        post = databaseutils.get_post_by_id(post_id)
        status = databaseutils.update_post_likes(post_id,user.id)
        return make_response(json.dumps(status),200)
    else:
        response = make_response(redirect(url_for('login')))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    
@app.route('/logout')
def logout():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token)):
        user = databaseutils.get_user_by_token(token)
        #remove token from user database
        response = make_response(redirect(url_for('index')))
        response.set_cookie('auth','',max_age=0,httponly=True)
        return response
    else:
        response = make_response(redirect(url_for('index')))
        response.set_cookie('auth','',max_age=0,httponly=True)
        return response

@app.route('/get_posts',methods=['POST'])
def getposts():
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token)):
        user = databaseutils.get_user_by_token(token=token)
        time = html.escape(request.json['time'])
        posts = databaseutils.get_all_posts()
        output = []
        for post in posts:
            obj = {'username':post.owner_username,'title':post.title,'content':post.content,'id':str(post.post_id),'like_count':post.like_count,'emoji':databaseutils.check_likes(post.post_id,user.id),'time_checked':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
            output.append(obj)
        return make_response(json.dumps(output),200)
    else:
        response = make_response(redirect(url_for('login')))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/profile/<string:user_id>')
def profile(user_id):
    token = request.cookies.get('auth',None)
    if(token !=None and databaseutils.check_token(token=token)):
        response = make_response(render_template('profile.html'),200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        return redirect(url_for('login'))

app.run(host='0.0.0.0',port=8080)