import os
from flask import Flask, make_response, send_from_directory, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send, rooms, emit, join_room, close_room, leave_room
import databaseutils
import bcrypt
import html
import secrets
import json
import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/catalog'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# File for all the server stuff
#########################################
# Sever Set Ups
app = Flask(__name__)
app.secret_key = 'SecretCodeHushHush'
app.config['SECRET'] = 'SecretCodeHushHush'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app, cors_allowed_orgins="*")
user_rooms = []

#############################
# Socket Stuff


@socketio.on('lobby_make')
def make_lobby(lobby):
    print('here')
    #'name': title, 'description': description, 'artists': artists, 'privacy': privacy}
    print(lobby)
    roomName = html.escape(lobby['name'])
    description = html.escape(lobby['description'])
    artists = html.escape(lobby['artists'])
    isPrivate = html.escape(lobby['privacy'])
    user_rooms.append(roomName)
    Image_url = "placeholder"
    print(user_rooms)
    print(isPrivate)
    if isPrivate == "public":
        print('is private is false')
        id = databaseutils.insert_lobby('test',roomName,description,Image_url,user_count=0,roomcode=None)
        emit('lobby_made', {'lobby_name': roomName, 'Description': description, 'artists': artists, 'id' : id,'count':0}, broadcast=True)
    else:
        id = databaseutils.insert_lobby('test',roomName,description,Image_url,roomcode=None)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)



@socketio.on('join lobby')
def test_message(message):
    join_room('lobby')
    print(rooms())
    emit('lobby joined', {'data': 'Connected to lobby'})

@socketio.on('update_count')
def test_message(count):
    users = databaseutils.get_users_in_room_by_id(count['lobby'])
    if(count['user'] not in users):
        databaseutils.add_user_to_lobby(count['lobby'],count['user'])
        item = databaseutils.get_lobby_by_id(count['lobby'])
        databaseutils.increase_lobby_count(count['lobby'])
        print(f'sending {count["lobby"]}')
        emit('count_update', {'count': item.count+1,'id':count['lobby']},broadcast=True)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


###############################
# Flask helper functions
def login_status(cookie):
    if cookie is not None:
        return databaseutils.check_token(cookie)
    return False


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_ext(filename):
    return '.' + filename.rsplit('.', 1)[1]


####################################################################
# Flask Routes


# Serving Static Files up with nosniff
@app.route('/<path:path>')
def send_static(path):
    response = make_response(send_from_directory('static', path), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/')
def index():
    response = make_response(render_template('index.html'), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if not login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('login.html', error=error), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            username = html.escape(request.form['username'])
            password = request.form['password']
            if not databaseutils.check_username_exists(username):
                response = make_response(render_template('login.html', error='Username or password incorrect',error1=None), 200)
                response.headers['X-Content-Type-Options'] = 'nosniff'
                return response
            else:
                if password is None or password == '' or password == ' ':
                    response = make_response(render_template('login.html', error='Password field empty',error1=None), 200)
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    return response
                else:
                    user = databaseutils.get_user_by_username(username)
                    passhash = bcrypt.hashpw(password.encode('utf-8'), user.salt)
                    if passhash == user.passhash:
                        response = redirect('lobby')
                        cookie = secrets.token_hex()
                        databaseutils.set_user_token(username, cookie)
                        response.set_cookie('auth', cookie, max_age=7200)
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        return response
                    else:
                        response = make_response(render_template('login.html', error='Username or password incorrect',error1=None),
                                                 200)
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        return response

    else:
        return redirect(url_for('lobby'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if not login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('login.html', error=None,error1=None), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            username = html.escape(request.form['newUsername'])
            password = request.form['newPassword']
            password2 = request.form['confirmPassword']
            if databaseutils.check_username_exists(username):
                response = make_response(render_template('login.html', error1='User already exists',error=None), 200)
                response.headers['X-Content-Type-Options'] = 'nosniff'
                return response
            else:
                if password is None or password == '' or password == ' ' or password != password2:
                    response = make_response(render_template('login.html', error1='Password empty or do not match',error=None),
                                             200)
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    return response
                else:
                    check = databaseutils.add_user(username, password)
                    if check:
                        resp = make_response(redirect('login'))
                        resp.headers['X-Content-Type-Options'] = 'nosniff'
                        return resp
                    else:
                        response = make_response(render_template('login.html', error1='Unable to add user',error=None), 200)
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        return response
    else:
        return redirect(url_for('lobby'))


@app.route('/createlobby')
def createlobby():
    if login_status(request.cookies.get('auth', None)):
        response = make_response(render_template('make_lobby.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response


@app.route('/lobby')
def lobby():
    if login_status(request.cookies.get('auth', None)):
        lobbies = databaseutils.get_lobbies()
        response = make_response(render_template('lobby.html',lobby=lobbies), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response


@app.route('/catalog')
def catalog():
    if login_status(request.cookies.get('auth', None)):
        images = databaseutils.get_images()
        response = make_response(render_template('catalog.html', images=images), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response


# Convert the flash things into error messages and retrun to the same page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('uploadcatalog.html'), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('upload'))
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('upload'))
            if file and allowed_file(file.filename):
                user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
                desc = 'Temp desc'
                igname = 'Temp image name'
                ext = get_ext(secure_filename(file.filename))
                # Filename needs to be generated into something unique... id from insert into database would work.
                filename = str(
                    databaseutils.save_image(username=user.username, image_description=desc, image_name=igname,
                                             ext=ext).inserted_id)
                # filename = secure_filename(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + ext))
                return redirect(url_for('dispfile', path=filename + ext))
            else:
                flash('Filetype not allowed')
                return redirect(url_for('upload'))

    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response


@app.route('/dispfile/<path:path>')
def dispfile(path):
    response = make_response(render_template('showimage.html', image_name=f'/catalog/{path}'), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/home-page',  methods=['GET', 'POST'])
def home_page():
    response = make_response(render_template('home_page.html'), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/lobby/<string:string>')
def lobbyin(string):
    if(request.cookies.get('lobby',None)!=None and request.cookies.get('lobby',None)!=string):
        if(databaseutils.get_lobby_by_id(request.cookies.get('lobby',None))==None):
            resp = make_response(redirect('/lobby/'+string))
            resp.headers['X-Content-Type-Options'] = 'nosniff'
            resp.set_cookie('lobby','',max_age=0) 
            return resp
        else:
            resp = make_response(redirect('/lobby/'+request.cookies.get('lobby',None)))
            resp.headers['X-Content-Type-Options'] = 'nosniff'
            return resp
    if login_status(request.cookies.get('auth', None)):
        user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
        response = make_response(render_template('game.html',code=string,users=databaseutils.get_users_in_room_by_id(string),user=user.username), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('lobby',string,max_age=7200)
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response

@app.route('/lobbycreate',methods=['POST'])
def lobbycreate():
    if login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('uploadcatalog.html'), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('upload'))
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('upload'))
            if file and allowed_file(file.filename):
                user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
                desc = 'Temp desc'
                igname = 'Temp image name'
                ext = get_ext(secure_filename(file.filename))
                # Filename needs to be generated into something unique... id from insert into database would work.
                filename = str(
                    databaseutils.save_image(username=user.username, image_description=desc, image_name=igname,
                                             ext=ext).inserted_id)
                # filename = secure_filename(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + ext))
                return redirect(url_for('dispfile', path=filename + ext))
            else:
                flash('Filetype not allowed')
                return redirect(url_for('upload'))

    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response

socketio.run(app=app, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)


