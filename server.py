import os
from flask import Flask, make_response, send_from_directory, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send, rooms, emit, join_room, close_room, leave_room
import databaseutils
import bcrypt
import html
import secrets
import time
import json
import datetime
import random
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



# brew services start mongodb/brew/mongodb-community
# brew services stop mongodb/brew/mongodb-community


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


#limiter = Limiter(get_remote_address, app=app,  storage_uri="mongodb://localhost:27017/group_project.rates",default_limits=["50 per 10 seconds"])
def lt(limiter):
        databaseutils.apply_rate(request.remote_addr)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri="memory://",
    default_limits=["500 per 10 seconds"],
    storage_options={"lockout": True, "lockout_time": 30},
    on_breach=lt
    )

test_limit = limiter.shared_limit("500 per 10 second", scope="global")





@app.after_request
def after_request(response):
    lockout_active = databaseutils.check_rate(request.remote_addr)
    print(request.remote_addr)
    if lockout_active:
        databaseutils.apply_rate(request.remote_addr)
        response.status_code = 429
        response.data = '429: Rate Limit Reached'
        response.headers['X-Content-Type-Options'] = 'nosniff'

    return response


#############################
# Socket Stuff


@socketio.on('lobby_make')
def make_lobby(lobby):
    #'name': title, 'description': description, 'artists': artists, 'privacy': privacy}
    roomName = html.escape(lobby['name'])
    description = html.escape(lobby['description'])
    artists = html.escape(lobby['artists'])
    isPrivate = html.escape(lobby['privacy'])
    user_rooms.append(roomName)
    Image_url = "placeholder"
    time.sleep(1)
    lob = databaseutils.get_lobby_by_host(lobby['host'])
    print(user_rooms)
    print(isPrivate)
    if isPrivate == "public":
        print('is private is false')
        #id = databaseutils.insert_lobby('test',roomName,description,Image_url,user_count=0,roomcode=None)
        emit('lobby_made', {'lobby_name': lob.title, 'Description': lob.desc, 'artists': artists, 'id' : str(lob.id),'count':0,'Image_url':lob.img}, broadcast=True)
    #else:
        #id = databaseutils.insert_lobby('test',roomName,description,Image_url,roomcode=None)


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

@socketio.on('winner')
def test_message(message):
    lobby = message['lobby']
    emit('end_game', {'user': message['user'],'value':message['value']},to=lobby)
    databaseutils.remove_lobby_by_id(lobby)

@socketio.on('update_count')
def test_message(count):
    time.sleep(1)
    join_room(count['lobby'])
    users = databaseutils.get_users_in_room_by_id(count['lobby'])
    if(count['user'] not in users):
        databaseutils.add_user_to_lobby(count['lobby'],count['user'])
        item = databaseutils.get_lobby_by_id(count['lobby'])
        databaseutils.increase_lobby_count(count['lobby'])
        it = random.randint(1,50)
        print(f'sending {count["lobby"]}')
        emit('count_update', {'count': item.count+1,'id':count['lobby']},broadcast=True)
        emit('update_users',{'user':count['user'],'count':item.count+1,'game_value':it,'max_player':item.max_player},to=count['lobby'])


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


#############################
    #Start Game
@socketio.on('start_game')
def Start_Game():
    emit('my response', {'data': 'Connected'})


###############################
# Flask helper functions
def login_status(cookie):
    if cookie is not None:
        print(cookie)
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
@test_limit
def send_static(path):
    response = make_response(send_from_directory('static', path), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/')
@test_limit
def index():
    response = make_response(render_template('index.html'), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/login', methods=['GET', 'POST'])
@test_limit
def login():
    if not login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('login.html'), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            username = html.escape(request.form['username'])
            password = request.form['password']
            if not databaseutils.check_username_exists(username):
                response = make_response(render_template('login.html', error='Username or password incorrect'), 200)
                response.headers['X-Content-Type-Options'] = 'nosniff'
                return response
            else:
                if password is None or password == '' or password == ' ':
                    response = make_response(render_template('login.html', error='Password field empty'), 200)
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    return response
                else:
                    user = databaseutils.get_user_by_username(username)
                    passhash = bcrypt.hashpw(password.encode('utf-8'), user.salt)
                    if passhash == user.passhash:
                        response = redirect('home-page')
                        cookie = secrets.token_hex()
                        databaseutils.set_user_token(username, cookie)
                        response.set_cookie('auth', cookie, max_age=7200)
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        return response
                    else:
                        response = make_response(render_template('login.html', error='Username or password incorrect'),
                                                 200)
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        return response

    else:
        return redirect(url_for('home_page'))


@app.route('/signup', methods=['GET', 'POST'])
@test_limit
def signup():
    error = None
    if not login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('login.html'), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            username = html.escape(request.form['newUsername'])
            password = request.form['newPassword']
            password2 = request.form['confirmPassword']
            email = request.form['newEmail']
            if databaseutils.check_username_exists(username):
                response = make_response(render_template('login.html', error1='User already exists'), 200)
                response.headers['X-Content-Type-Options'] = 'nosniff'
                return response
            else:
                if password is None or password == '' or password == ' ' or password != password2:
                    response = make_response(render_template('login.html', error1='Password empty or do not match'),
                                             200)
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    return response
                else:
                    check = databaseutils.add_user(username, password, email)
                    if check:
                        resp = make_response(redirect('login'))
                        resp.headers['X-Content-Type-Options'] = 'nosniff'
                        return resp
                    else:
                        response = make_response(render_template('login.html', error1='Unable to add user'), 200)
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        return response
    else:
        return redirect(url_for('lobby'))


@app.route('/createlobby')
@test_limit
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
@test_limit
def lobby():
    if login_status(request.cookies.get('auth', None)):
        lobbies = databaseutils.get_lobbies()
        response = make_response(render_template('lobby.html',lobby=lobbies,error=None), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response


@app.route('/catalog')
@test_limit
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
@test_limit
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

@app.route('/verify/<string:string>')
@test_limit
def verify(string):
    if(string!=None):
        check = databaseutils.update_user_by_vcode(string)

        if check:
            response = make_response('Successfully Verified Account', 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            response = make_response('Invalid Verification Code or User already Verified', 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
    else:
        response = make_response('Invalid Verification Code or User already Verified', 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/profile')
@test_limit
def profile():
    if login_status(request.cookies.get('auth', None)):
        user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
        response = make_response(render_template('profile.html',user=user.username,vef = user.email_verified), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response

@app.route('/dispfile/<path:path>')
@test_limit
def dispfile(path):
    response = make_response(render_template('showimage.html', image_name=f'/catalog/{path}'), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/home-page',  methods=['GET', 'POST'])
@test_limit
def home_page():
    if login_status(request.cookies.get('auth', None)):
        user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
        response = make_response(render_template('home_page.html',user=user.username), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response
    

@app.route('/rick-roll', methods = ['GET'])
@test_limit
def rick_roll():
    if login_status(request.cookies.get('auth', None)):
        user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
        response = make_response(render_template('rickroll.html',user=user.username), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response


@app.route('/lobby/<string:string>')
@test_limit
def lobbyin(string):
    if login_status(request.cookies.get('auth', None)) == False:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response
    if(request.cookies.get('lobby',None)!=None and request.cookies.get('lobby',None)!=string):
        if(databaseutils.get_lobby_by_id(request.cookies.get('lobby',None))==None):
            resp = make_response(redirect('/lobby/'+string))
            resp.headers['X-Content-Type-Options'] = 'nosniff'
            resp.set_cookie('lobby','',max_age=0) 
            return resp
        else:
            lobby = databaseutils.get_lobby_by_id(string)
            if(int(lobby.count)<int(lobby.max_player)):
                resp = make_response(redirect('/lobby/'+request.cookies.get('lobby',None)))
                resp.headers['X-Content-Type-Options'] = 'nosniff'
                return resp
            else:
                resp = make_response(redirect('/lobby'))
                resp.headers['X-Content-Type-Options'] = 'nosniff'
                return resp
    lobby = databaseutils.get_lobby_by_id(string)
    if(int(lobby.count)>=int(lobby.max_player)):
            if(request.cookies.get('lobby',None)==string):
                print('1')
                if login_status(request.cookies.get('auth', None)):
                    user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
                    response = make_response(render_template('game.html',code=string,users=databaseutils.get_users_in_room_by_id(string),user=user.username), 200)
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    #response.set_cookie('lobby',string,max_age=7200)
                    return response

            else:
                print('2')
                resp = make_response(redirect('/lobby'))
                resp.headers['X-Content-Type-Options'] = 'nosniff'
                return resp
    else:
        if login_status(request.cookies.get('auth', None)):
            print(databaseutils.get_lobby_by_id(string).count)
            print('3')
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
@test_limit
def lobbycreate():
    if login_status(request.cookies.get('auth', None)):
        if request.method == 'GET':
            response = make_response(render_template('uploadcatalog.html'), 200)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
        else:
            user_sess = request.cookies.get('lobby',None)
            if user_sess!=None:
                t = databaseutils.get_lobby_by_id(user_sess)
                if(t!=None):
                    return redirect(url_for('lobbyin',string=user_sess))
            
            # check if the post request has the file part
            if 'file' in request.files and request.files['file'].filename != '' and allowed_file(request.files['file'].filename):
                user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
                desc = 'Temp desc'
                igname = 'Temp image name'
                file = request.files['file']
                ext = get_ext(secure_filename(file.filename))
                # Filename needs to be generated into something unique... id from insert into database would work.
                filename = str(
                    databaseutils.save_image(username=user.username, image_description=desc, image_name=igname,
                                             ext=ext).inserted_id)
                # filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + ext))
                title = request.form.get('title')
                desc = request.form.get('description')
                max = request.form.get('artists')

                id = databaseutils.insert_lobby(user.username,title,desc,filename + ext,max,user_count=0)
                return redirect(url_for('lobbyin', string=id))
            else:
                max = request.form.get('artists')
                user = databaseutils.get_user_by_token(request.cookies.get('auth', None))
                title = request.form.get('title')
                desc = request.form.get('description')
                id = databaseutils.insert_lobby(user.username,title,desc,'logo.png',max,user_count=0)
                
                return redirect(url_for('lobbyin', string=id))

    else:
        response = make_response(redirect('login'))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.set_cookie('auth', '', max_age=0)
        return response
    

    #Routes for the pack making stuff
@app.route('/packs')
@test_limit
def packs():
    pack_list = databaseutils.get_all_packs()
    print(pack_list)
    response = make_response(render_template('packs.html',pack_list=pack_list), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/make_pack',methods=['GET','POST'])
@test_limit
def make_pack():
    if request.method == 'GET':
        response = make_response(render_template('make_pack.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    else:
        print('Making Pack')
        response = make_response(render_template('make_pack.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/view_pack/<path:path>',methods=['GET','POST'])
@test_limit
def view_pack(path):
    pack = databaseutils.get_pack_by_path(path=path)
    if request.method == 'GET':
        response = make_response(render_template('view_pack.html',pack=pack), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

###################
    #TEMP PATHS FOR DESIGN
@app.route('/gamewip',methods=['GET','POST'])
@test_limit
def gamewip():
    if request.method == 'GET':
        response = make_response(render_template('gamewip.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/gameinprg',methods=['GET','POST'])
@test_limit
def gameinprg():
    if request.method == 'GET':
        response = make_response(render_template('gameinprogress.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
@app.route('/gameresults',methods=['GET','POST'])
@test_limit
def gameresults():
    if request.method == 'GET':
        response = make_response(render_template('gameresults.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

@app.route('/endgame',methods=['GET','POST'])
@test_limit
def endgame():
    if request.method == 'GET':
        response = make_response(render_template('endgame.html'), 200)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response



#socketio.run(app=app, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
        #socketio.run(app=app,host='0.0.0.0',allow_unsafe_werkzeug=True)
        socketio.run(app=app, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)
        #app.run()
