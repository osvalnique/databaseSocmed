from Models import Users
from flask import request
from . import db
import bcrypt

# create user
# change pw user
# deactivate user
# search user
# follow other user
# unfollow other user

# check users activity *
# ban users *

def get_all():
    users = Users.query.all()
    
    return [{"username" : user.username} for user in users]

def get_user(id):
    user = Users.query.filter_by(user_id = id).first_or_404()
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"username" : user.name,
            "following_count" : following_count,
            "following" : [u.name for u in user.following_list],
            "followers_count" : followers_count,
            "followers" : [u.name for u in user.follower_list]}
    
def get_username(username):
    user = Users.query.filter_by(username = username).first_or_404()
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"username" : user.name,
            "following_count" : following_count,
            "following" : [u.name for u in user.following_list],
            "followers_count" : followers_count,
            "followers" : [u.name for u in user.follower_list]}

def create_users():
    data = request.get_json()
    
    data['password'] = str(data['password']).encode('utf-8')
    hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
    hashed = hashed.decode('utf-8')
    
    u = Users(
        name = data['name'],
        email = data['email'],
        username = str(data['username']).lower(),
        password = hashed,
        bio = data['bio']
    )
    
    db.session.add(u)
    # db.session.commit()
    
    return 'Account Created Successfully', 201

def change_username(id):
    data = request.get_json()
    user = Users.query.filter_by(user_id=id).first_or_404()
    
    if user.username != data['username']:
        u = Users.query.filter_by(username = data['username']).first()
        if u != None :
            return 'Username Already Exist', 400
        user.username = data['username']
        
        db.session.commit()
        return 'Username Changed Successfully'
    
    return 'Please Insert Different Username', 400

    
    