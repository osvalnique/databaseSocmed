import os
from uuid import uuid4
from Models import Users, Tweet
from Models.modelsUsers import Role, Status
from flask import abort, request, g
from sqlalchemy import text
from flask_jwt_extended import current_user
from . import db
from werkzeug.utils import secure_filename
import bcrypt
import re

def get_all():
    user = Users.query.all()
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"result" :
            {"username" : user.username,
            "name" : user.name,
            "following_count" : following_count,
            "followers_count" : followers_count,
            "profile_picture" : user.img_url
            }}

def get_user(id):
    user = Users.query.filter_by(user_id = id).first_or_404()
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"result" :
            {"username" : user.username,
            "name" : user.name,
            "following_count" : following_count,
            "followers_count" : followers_count,
            "profile_picture" : user.img_url
            }}
    
def get_username(username):
    user = Users.query.filter_by(username = username).first_or_404()
    tweet = Tweet.query.filter_by(user_id = user.user_id).all()
    tweet_count = len(tweet)
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"result" :
            {"username" : user.username,
            "bio" : user.bio,
            "name" : user.name,
            "following_count" : following_count,
            "followers_count" : followers_count,
            "tweet_count" : tweet_count,
            "profile_picture" : user.img_url
            }}
    
def get_following_list(username):
    user = Users.query.filter_by(username = username).first_or_404()
    
    return {"result" : 
            {"following" : [u.username for u in user.following_list]
            }}

def get_followed_list(username):
    user = Users.query.filter_by(username = username).first_or_404()
    
    return {"result" :
            {"followers" : [u.username for u in user.follower_list]
            }}
    
def get_last_login():
    last_login = text("SELECT USERNAME , LAST_LOGIN FROM USERS U \
        WHERE LAST_LOGIN <= now() - INTERVAL '2' MONTH ;")
    result = db.engine.connect().execute(last_login).mappings().all()
    return {"result" : 
            [{"username" : user.username,
             "last_login" : user.last_login} for user in result]}
    
def follow(followed_id):
    user_id = current_user.user_id
    followed_user = Users.query.filter_by(user_id = followed_id).first()
    
    if followed_user == None:
        return {"msg" : 'User is Not Found'}, 400
    
    if followed_user.user_id == user_id:
        return {"msg" : 'Please Insert Different Username'},400
    
    if followed_user in current_user.following_list:
        return {"msg" : 'Account Already Followed'},400
    
    else :
        current_user.following_list.append(followed_user)
        
        db.session.commit()
        return {"msg" : f'Now You Are Following {followed_user.username}'}
    
def unfollow(followed_id):
    followed_user = Users.query.filter_by(user_id = followed_id).first()
    
    if followed_user == None:
        return {"msg" : 'User is Not Found'}, 400
    
    if followed_user not in current_user.following_list:
        return {"msg" : 'You Are not Following Yet'}, 400
    
    for i in range(len(current_user.following_list)):
        if current_user.following_list[i].user_id == followed_user.user_id:
            print(current_user.following_list[i].user_id, followed_user.user_id)
            current_user.following_list.pop(i)
            print(i)
            break
        
    db.session.commit()
        
    return {"msg" : f'You Are Unfollowed {followed_user.username}'}
    
def get_following_tweets():
    tweets = text('SELECT * FROM TWEETS T \
        JOIN USERS U ON u.USER_ID = t.USER_ID \
        WHERE t.USER_ID IN (SELECT followed FROM FOLLOW F)\
        ORDER BY t.CREATED_AT DESC;')
    result = db.engine.connect().execute(tweets).mappings().all()
    print(result)
    return 'test'
    # return [{'tweet' : t.tweet,
    #          'posted_by' : t.username,
    #          'created_at' : t.created_at} for t in result]
            
def create_users():
    data = request.form
    data_img = request.files['img']
    filename = uuid4().hex + secure_filename(data_img.filename)
    data_img.save(os.path.join('uploadedImg', filename))
    path_img = os.path.join('uploadedImg', filename)
    
    user = Users.query.filter_by(email = data.get('email')).first()
    
    pattern = r'^[a-zA-Z0-9_.+-]{6,}@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    is_match = bool(re.match(pattern, data.get('email')))
    
    if user != None:
        return {"msg" : 'Email is Already Registered'}, 400
        
    username = Users.query.filter_by(username = data.get('username')).first()
    if username != None:
        return {"msg" : 'Username Already Exist'}, 400
        
    if is_match == False:
        return {"msg" : 'Please Enter Valid email'}, 400
    
    if len(data.get('password')) < 8:
        return {"msg" : 'Password Must Contains at Least 8 Characters'}, 400
    
    password = str(data.get('password')).encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed = hashed.decode('utf-8')
    
    u = Users(
        name = data.get('name'),
        email = data.get('email'),
        username = str(data.get('username')).lower(),
        password = hashed,
        bio = data.get('bio'),
        img_url = path_img
    )

    db.session.add(u)
    db.session.commit()
    
    return {"msg" : 'Account Created Successfully'}, 201

def change_role(user_id):
    developer = str(current_user.role)
    user = Users.query.filter_by(user_id =user_id).first()
    print(developer)
    print(user.role)
    
    if str(user.role) == "Role.developer":
        return {"msg" : "You are a Developer"}
    
    else :
        user.role = Role.developer
        db.session.commit()
        return {"msg" : f'Now {user.username} is Developer'}

def update_user():
    id = current_user.user_id
    data = request.get_json()
    user = Users.query.filter_by(user_id=id).first_or_404()
           
    if user.username != data['username']:
        u = Users.query.filter_by(username = data['username']).first()
        if u != None :
            return {"msg" : 'Username Already Exist'}, 400
        user.username = data['username']
        
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed
  
    db.session.commit()
    
    return {"msg" : 'User Updated Successfully'}, 201

def update_image():
    new_img = request.files.get('new_img')
    current_img = current_user.img_url

    if new_img == None:
        print(new_img)
        return {"msg": 'Please Import an Image'}
    
    filename = uuid4().hex + secure_filename(new_img.filename)
    format = filename.rsplit('.', 1)[1].lower()
    
    if format in {'png', 'jpg', 'jpeg', 'gif'}:
        path_img = os.path.join('uploadedImg', filename)
        new_img.save(path_img)
    
        if current_img:
            old_path = os.path.join('uploadedImg', current_img)
            if os.path.exists(old_path):
                os.remove(old_path)
            
        current_user.img_url = filename
        db.session.commit()
        return {"msg": "Image Uploaded"}, 200
    
    return {"msg" : f"Does Not Support {format} Format"}

    
def deactivate_user():
    id = current_user.user_id
    user = Users.query.filter_by(user_id = id).first_or_404()
    
    if user.status == Status.active:
        user.status = 'inactive'
        db.session.commit()
        return {"msg" : "User Deactivate"}, 200
    
    if user.status == Status.inactive:
        return {"msg" : "User is Inactive"}, 400
    
    else :
        return {"msg" : "User Banned"}, 400
    
def activate_user():
    id = current_user.user_id
    user = Users.query.filter_by(user_id = id).first_or_404()
    
    if user.status == Status.inactive:
        user.status = 'active'
        db.session.commit()
        return {"msg" :'User Activate'}, 200
    
    if user.status == Status.active:
        return {"msg" : "User is Active"}, 400
    
    else :
        return {"msg" : "User Banned"}, 400
    
def ban_user(id):
    user_id = current_user.user_id
    user = Users.query.filter_by(user_id=id).first_or_404()
    
    if user == None:
        return {"msg" : 'User is Not Found'}, 400
    
    if user.status == Status.active or user.status == Status.inactive:
        user.status = 'banned'
        db.session.commit()
        return {"msg" : f'User {user.username} is Suspended'}, 200
    
    return {"msg" : f'{user.username} Already Banned'}, 400
    
def unban_user(id):
    user_id = current_user.user_id
    user = Users.query.filter_by(user_id=id).first_or_404()
    
    if user.status == Status.banned:
        user.status = 'active'
        db.session.commit()
        return {"msg" : f'User {user.username} is Reactivated'}, 200
    
    return {"msg" : f'{user.username} Already Active'}, 400
    
def most_followers():
    followers = text('SELECT username, x.followers \
        FROM \
        (SELECT FOLLOWED, count(FOLLOWED) followers \
        FROM FOLLOW F GROUP BY followed) x\
        JOIN USERS U ON u.USER_ID = x.followed \
        ORDER BY x.followers DESC\
        LIMIT 5;')
    result = db.engine.connect().execute(followers).mappings().all()

    return {'results' : [dict(f) for f in result]}
        
     
    
    
    
    

    
    