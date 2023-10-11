from Models import Users, Tweet
from Models.modelsUsers import Status
from flask import abort, request, g
from sqlalchemy import text
from . import db
import bcrypt

# create user DONE
# search user DONE
# deactivate user DONE
# follow other user DONE
# unfollow other user DONE
# change pw user
# most followers

# check users inactive *
# ban users *

def get_all():
    tweets = Tweet.query.all()

    return [{"tweet": t.tweet,
            "posted_by" : t.user.username} 
            for t in tweets], 200

def get_user(id):
    user = Users.query.filter_by(user_id = id).first_or_404()
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"username" : user.name,
            "following_count" : following_count,
            "following" : [u.name for u in user.following_list],
            "followers_count" : followers_count,
            "followers" : [u.name for u in user.follower_list]}
    
def get_last_login():
    last_login = text("SELECT USERNAME , LAST_LOGIN FROM USERS U \
        WHERE LAST_LOGIN <= now() - INTERVAL '2' MONTH ;")
    result = db.engine.connect().execute(last_login).mappings().all()
    return [{"username" : user.username,
             "last_login" : user.last_login} for user in result]
    
def follow():
    data = request.get_json()
    
    if 'follow_id' not in data or 'followed_id' not in data:
        return 'Input follow_id and followed_id'
    follow_user = Users.query.filter_by(user_id=data['follow_id']).first()
    
    if data['follow_id'] == data['followed_id']:
        return 'follow_id and followed_id must be different'
    
    if follow_user == None:
        return 'User Not Found', 404
    
    followed_user = Users.query.filter_by(user_id=data['followed_id']).first()
    if followed_user == None:
        return 'User Not Found', 404
    
    found = False
    for i in range(len(follow_user.following_list)):
        if follow_user.following_list[i].user_id == followed_user.user_id:
            follow_user.following_list.pop(i)
            print(followed_user.following_list)
            found = True
            msg = f'You are unfollow {followed_user.username}'
            break
    if found == False:
        follow_user.following_list.append(followed_user)
        msg = f'You are following {followed_user.username}'
    db.session.commit()
    return msg
    
            
def get_profile(username):
    user = Users.query.filter_by(username = username).first_or_404()
    tweet_user = text("SELECT TWEET, USERNAME  FROM TWEETS T\
        JOIN USERS U  ON U.USER_ID  = T.USER_ID")
    result = db.engine.connect().execute(tweet_user).mappings().all()
    print(result)
    
    following_count = len(user.following_list)
    followers_count = len(user.follower_list)
    
    return {"username" : user.name,
            "following_count" : following_count,
            "following" : [u.name for u in user.following_list],
            "followers_count" : followers_count,
            "followers" : [u.name for u in user.follower_list],
            "tweets" : result}

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
        bio = data['bio'],
    )
    # # print(data)
    # if Users.role == "developer":
    #     role = data['role']
        
    #     return role
    db.session.add(u)
    db.session.commit()
    
    return 'Account Created Successfully', 201

def update_user(id):
    data = request.get_json()
    user = Users.query.filter_by(user_id=id).first_or_404()
    
    if g.user.user_id != id:
        abort(401, "Username doesn't match with id")
        
    if user.username != data['username']:
        u = Users.query.filter_by(username = data['username']).first()
        if u != None :
            return 'Username Already Exist', 400
        user.username = data['username']
        
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed
    # user.password = data['password']
    print(data['password'])
    db.session.commit()
    
    
    g.pop('user')

    return 'User Updated Successfully'



def deactivate_user(id):
    
    user = Users.query.filter_by(user_id = id).first_or_404()
    print(type(user.status))
    
    if user.status == Status.inactive:
        user.status = 'active'
        db.session.commit()
        return 'User Activate', 200
    
    elif user.status == Status.active:
        user.status = 'inactive'
        db.session.commit()
        return 'User Deactivate', 200
    
    else :
        return 'User Banned', 400
    
def ban_user(id):
    user = Users.query.filter_by(user_id=id).first_or_404()
    
    if user.status == Status.active or user.status == Status.inactive:
        user.status = 'banned'
        db.session.commit()
        return f'User {user.username} is Suspended', 200
    
    elif user.status == Status.banned:
        user.status = 'active'
        db.session.commit()
        return f'User {user.username} is Reactivated', 200
     
    
    
    
    

    
    