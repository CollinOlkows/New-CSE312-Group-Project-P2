from pymongo import MongoClient
import bcrypt
import datetime
import html
from hashlib import sha256
from bson.objectid import ObjectId
import server_utils
import random
import os
#mongo_client = MongoClient("mongo")
mongo_client = MongoClient("localhost")
db = mongo_client["group_project"]
users = db['users']
posts = db['posts']
comments = db['comments']
lobbys = db['lobbys']
images = db['images']
users_in = db['users_in']
rates = db['rates']
db_packs = db['packs']

deloyed_mode = False



#Comments and posts have become obsolete for this project. Will Be updated at a later time

'''
users -> {username:username,passhash:passwordhash,salt:passwordsalt,_id:user_id,followers,following,token,exp_date}
posts ->{_id:post_id,post_owner:user_id,content:content,creation_date:date,likes:[User_id],owner_username:username,comments:[Comment]}
comments ->{_id:comment_id,content:comment_content,date:creation_date,type:Parent or Child(thread or reply),post_origin,comment_owner,owner_username}
lobby -> {'host':host,'title':title,'desc':desc,'img_url':img_url,'user_count':user_count}
images - > {'username':username,'description':image_description,'image_name':image_name}
rates -> {'address':address,'locked':false,exp_time:time}
'''

#wrappers for easy working with users

class user:
    def __init__(self,user_obj):
        self.username = user_obj['username']
        self.passhash = user_obj['passhash']
        self.salt = user_obj['salt']
        self.id = user_obj['_id']
        self.followers = user_obj['followers']
        self.following = user_obj['following']
        self.token = user_obj['token']
        self.token_date = user_obj['token_date']
        self.email = user_obj['email']
        self.email_verified = user_obj['email_verified']
        self.verification_code = user_obj['veri']

class lobby:
    def __init__(self,lobby_obj):
        self.host = lobby_obj['host']
        self.id = str(lobby_obj['_id'])
        self.title = lobby_obj['title']
        self.desc = lobby_obj['desc']
        self.img = lobby_obj['img_url']
        self.count = lobby_obj['user_count']
        self.roomcode = lobby_obj['roomcode']

class img:
    def __init__(self,image_obj):
        self.username = image_obj['username']
        self.id = image_obj['_id']
        self.desc = image_obj['description']
        self.name = image_obj['image_name']
        self.ext = image_obj['ext']
        self.fp = '/catalog/'+str(image_obj['_id'])+image_obj['ext']

#wrappers for easy working with posts
class post:
    def __init__(self,post_obj):
        self.post_id = post_obj['_id']
        self.post_owner = post_obj['post_owner']
        self.title = post_obj['title']
        self.content = post_obj['content']
        self.creation_date = post_obj['creation_date']
        self.likes = post_obj['likes']
        self.like_count = len(self.likes)
        self.owner_username = post_obj['owner_username']
        self.comments = post_obj['comments']

class comment:
    def __init__(self,person,content):
        self.person = person
        self.creation_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.content = content


class pack:
    def __init__(self,pack_object):
        self.path = pack_object['path']
        self.packs_directory = './static/images/packs/' + pack_object['path']
        self.owner = pack_object['username']
        self.icon = 'logo.png'
        self.public = pack_object['public']
        self.description = None
        self.pack_name = pack_object['pack_name']
        self.id = pack_object['_id']
        self.deck = os.listdir(self.packs_directory)

    def print_attb(self):
        print(f'Directory: {self.packs_directory}\nPack Name: {self.pack_name}\nOwner: {self.owner}\nImage List {self.deck}\nID: {self.id}')
        return 'Attributes Listed'


def get_all_packs():
    pack_list = []
    packs = db_packs.find({})
    for p in packs:
        pack_list.append(pack(p))
    return pack_list

def get_pack_by_username_and_pack_name(username,pack_name):
    check = db_packs.find_one({'username':username,'pack_name':pack_name})
    if(check != None):
        return pack(check)
    else:
        return None

def make_default_pack():
    check = db_packs.find_one({'username':'collin','pack_name':'default'})
    if check == None:
        db_packs.insert_one({'username':'collin','pack_name':'default','icon':None,'path':'default','description':'Official Default Pack','public':True})
        return True
    return False

#Creates a pack where the username is the creater and the name of the pack is an html escaped title with optional icon image
def create_empty_pack(username,pack_name,description,public,icon = None, path = None):
    check = db_packs.find_one({'username':username,'pack_name':pack_name})
    if check == None:
        insert = db_packs.insert_one({'username':username,'pack_name':pack_name,'icon':icon,'description':description,'public':public})
        if(path == None):
            new_path = str(insert.inserted_id)
            #path will always be the './static/images/packs/' + pack folder name.... these will not be named by the user except default
            os.makedirs('./static/images/packs/'+new_path)
            obj1 = db_packs.update_one({'username':username,'pack_name':pack_name},{'$set':{'path':new_path}})
            return pack(obj1)
        else:
            obj1 = db_packs.update_one({'username':username,'pack_name':pack_name},{'$set':{'path':path}})
            return pack(obj1)
    else:
        return False

def apply_rate (addy):
    check = rates.find_one({'address':addy})
    if(check==None):
        rates.insert_one({'address':addy,'locked':True,'exp':datetime.datetime.now()+datetime.timedelta(seconds=30)})
    else:
        if(datetime.datetime.now()>check['exp']):
            rates.find_one_and_delete({'address':addy})
            rates.insert_one({'address':addy,'locked':True,'exp':datetime.datetime.now()+datetime.timedelta(seconds=30)})
            
def check_rate(addy):
    check = rates.find_one({'address':addy})
    if(check!=None):
        if(datetime.datetime.now()>check['exp']):
            rates.find_one_and_update({'address':addy},{'$set':{'locked':False}})
            return False
        return True
    else:
        return False

#adds a user to the database if one does not exist
def add_user(username,password, email):
    check = users.find_one({'username':username})
    if(check != None):
        return False
    else:
        salt = bcrypt.gensalt()
        passhash = bcrypt.hashpw(password.encode('utf-8'),salt)
        code = server_utils.make_url_for_ver()
        users.insert_one({'username':username,'passhash':passhash,'salt':salt,'followers':[],"following":[],'token':'','token_date':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'email':email,'email_verified':False,'veri':code})
        #send verification email
        if deloyed_mode:
            server_utils.verification_email(code,username,email)
        return True

def update_user_by_vcode(code):
    user_found = users.find_one({'veri':code})
    if(user_found == None):
        return False
    else:
        u = user(user_found)
        update_user_email_verification_by_username(u.username)
        return True

#updates the users password, Requires users Username
def update_user_email_verification_by_username(username):
    user = users.find_one_and_update({'username':username},{"$set":{'email_verified':True,'veri':None}})
    return user

#updates the users password, Requires users ID
def update_user_email_verification_by_id(id):
    user = users.find_one_and_update({'_id':ObjectId(id)},{"$set":{'email_verified':True}})
    return user

#updates the users password, Requires users Username
def update_user_pass_by_username(username,password):
    salt = bcrypt.gensalt()
    passhash = bcrypt.hashpw(password.encode('utf-8'),salt)
    user = users.find_one_and_update({'username':username},{"$set":{'passhash':passhash,'salt':salt}})
    return user

#updates the users password, Requires users ID
def update_user_pass_by_id(id,password):
    salt = bcrypt.gensalt()
    passhash = bcrypt.hashpw(password.encode('utf-8'),salt)
    user = users.find_one_and_update({'_id':ObjectId(id)},{"$set":{'passhash':passhash,'salt':salt}})
    return user

#Gets the user and returns a user object if found or none if not using the users username
def get_user_by_username(username):
    user_found = users.find_one({'username':username})
    if(user_found != None):
        return user(user_found)
    else:
        return None

#gets the user by their id and returns a user object if found or none if not
def get_user_by_id(id):
    user_found = users.find_one({'_id':ObjectId(id)})
    if(user_found != None):
        return user(user_found)
    else:
        return None

#Gets a users id from their username
def get_id_by_username(username):
    user_found = users.find_one({'username':username})
    if(user_found != None):
        return user_found['_id']
    else:
        return None

#Gets a users username from their id
def get_username_by_id(id):
    user_found = users.find_one({'_id':ObjectId(id)})
    if(user_found != None):
        return user_found['username']
    else:
        return None

#Returns a list of post objects that a specific id created
def get_all_posts_by_user_id(id):
    all_posts = posts.find({'post_owner':ObjectId(id)})
    output = []
    if(all_posts!=None):
        for p in all_posts:
            output.append(post(p))
    else:
        return None

#Returns a list of post objects that a specific user created
def get_all_posts_by_username(username):
    all_posts = posts.find({'owner_username':username})
    output = []
    if(all_posts!=None):
        for p in all_posts:
            output.append(post(p))
    else:
        return None

def delete_all_posts_by_username(username):
    return posts.delete_many({"owner_username":username})

def delete_all_posts_by_user_id(*id):
    return posts.delete_many({"post_owner":ObjectId(id)})
#----------------------------------------- 
#if the user is deleted, posts are not, do we want all posts to also be deleted?
#deletes a user by their id
#Need to add an unfollow + Mass Unfollow
def user_delete_by_id(id):
    delete_all_posts_by_user_id(id=id)
    return users.delete_one({'_id':ObjectId(id)})

#deletes a user by their username 
def user_delete_by_username(username):
    delete_all_posts_by_username(username=username)
    return users.delete_one({'username':username})

def add_post(user,content,title):
    #idk if dateime is correct here
    return posts.insert_one({'post_owner':user.id,'content':content,'title':title,'owner_username':user.username,'creation_date':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'likes':[],'comments':[]})

def get_post_by_id(id):
    return posts.find_one({'_id':ObjectId(id)})

def update_post_by_id(id,content):
    return posts.update_one({'_id':ObjectId(id)},{"$set":{'content':content}})

#like value is either 1 or -1 (like or dislike)
def check_likes(id,user_id):
    p = get_post_by_id(id=id)
    if(p != None):
        likes = p['likes']
        if user_id in likes:
            return '❤️'
        else:
            return '🖤'
    else:
        return '🖤'


def update_post_likes(id,user_id):
    p = get_post_by_id(id=id)
    if(p != None):
        likes = p['likes']
        if user_id in likes:
            likes.remove(user_id)
            posts.update_one({'_id':ObjectId(id)},{"$set":{'likes':likes}})
            return {'status':'User Unliked','liked':False,'likes':len(likes),'emoji':'🖤'}
        else:
            likes.append(user_id)
            posts.update_one({'_id':ObjectId(id)},{"$set":{'likes':likes}})
            return {'status':'User liked','liked':True,'likes':len(likes),'emoji':'❤️'}
    else:
        return None

#Maybe Change this to add comment id to post rather than whole object, so its a list of comments in order of posts
#comment will have attribute of being a thread or reply to thread

def add_comment_to_post(id,comment_obj):
    p = get_post_by_id(id=id)
    if(p != None):
        comments = p['comment']
        comments.append(comment_obj)
        return posts.update_one({'_id':ObjectId(id)},{"$set":{'comment':comments}})
    else:
        return None

def get_all_posts():
    p = posts.find()
    out = []
    for po in p:
        out.append(post(po))
    return out

def delete_post_by_id(id):
    return posts.delete_one({"_id":ObjectId(id)})

#needs to remove from post list and if parent, delete all replys to said post
def delete_comment():
    pass

def set_user_token(username,token,date=datetime.datetime.now()):
    hash = sha256(token.encode('utf-8')).hexdigest()
    return users.update_many({'username':username},{"$set":{'token':str(hash),"token_date":date}})

def get_user_by_token(token):
    hash = sha256(token.encode('utf-8')).hexdigest()
    u = users.find_one({'token':hash})
    if u != None:
        return user(u)
    else:
        return None

def check_username_exists(username):
    test = users.find_one({'username':username})
    if(test == None):
        return False
    else:
        return True

def check_token(token):
    hash = sha256(token.encode('utf-8')).hexdigest()
    u = users.find_one({'token':hash})
    if u != None:
        if token == 'expired':
            #remove token
            return False
        else:
            return True
    else:
        return False
    
def save_image(username,image_description,image_name,ext):
    return images.insert_one({'username':username,'description':image_description,'image_name':image_name,'ext':ext})

def get_images():
    image = images.find()
    out = []
    for im in image:
        out.append(img(im))
    return out

def insert_lobby(host,title,desc,img_url,user_count=1,roomcode=None):
    id = str(lobbys.insert_one({'host':host,'title':title,'desc':desc,'img_url':img_url,'user_count':user_count,'roomcode':roomcode}).inserted_id)
    users_in.insert_one({'room': id,'users':[]})
    return id

def get_lobbies():
    lob = lobbys.find({'roomcode':None})
    out = []
    for l in lob:
        out.append(lobby(l))
    return out

def get_lobby_by_host(host):
    find = lobbys.find_one({'host':host})
    print(find)
    if(find!=None):
        return lobby(find)
    else:
        return None

def get_lobby_by_id(id):
    obj_id = ObjectId(id)
    find = lobbys.find_one({'_id':obj_id})
    if(find!=None):
        return lobby(lobbys.find_one({'_id':obj_id}))
    else:
        return None

def get_lobby_by_roomcode(code):
    return lobby(lobbys.find_one({'roomcode':code}))

def remove_lobby_by_id(id):
    id_obj= ObjectId(id)
    rem = lobbys.find_one_and_delete({'_id':id_obj})
    if(rem != None):
        return True
    else:
        return False

def remove_lobby_by_host(host):
    rem = lobbys.find_one_and_delete({'host':host})
    if(rem != None):
        return True
    else:
        return False
    
def remove_lobby_by_roomcode(roomcode):
    if(roomcode != None):
        rem = lobbys.find_one_and_delete({'roomcode':roomcode})
        if(rem != None):
            return True
        else:
            return False
    else:
        return False

def increase_lobby_count(id):
    lob = get_lobby_by_id(id)
    return lobbys.find_one_and_update({'_id':ObjectId(id)},{'$set':{'user_count':lob.count+1}})

def decrease_lobby_count(id):
    lob = get_lobby_by_id(id)
    return lobbys.find_one_and_update({'_id':ObjectId(id)},{'$set':{'user_count':lob.count-1}})

def get_users_in_room_by_id(id):
    return users_in.find_one({'room':id})['users']

def add_user_to_lobby(id,user):
    u = users_in.find_one({'room':id})
    us = u['users']
    if(user not in us):
        us.append(user)
    users_in.find_one_and_update({'room':id},{'$set':{'users':us}})
    return

def remove_user_from_lobby(id,user):
    u = users_in.find_one({'room':id})
    us = u.users_in
    us.remove(user)
    users_in.find_one_and_update({'room':id},{'$set':{'users':us}})
    return

def get_image_by_username(username):
    find = img(lobbys.find_one({'username':username}))
    if(find!=None):
        return img(find)
    else:
        return None