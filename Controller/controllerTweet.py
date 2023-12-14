from datetime import datetime
import os
from uuid import uuid4
from sqlalchemy import text
from Models import Tweet, Users
from flask import request
from flask_jwt_extended import current_user
from werkzeug.utils import secure_filename
from . import db

def get_all():
    tweets = Tweet.query.all()
    
    return [{"tweet" : tweet.tweet,
             "posted_by" : tweet.user.username,
             "created_at" : tweet.created_at} for tweet in tweets]

def get_tweet_user_id(user_id):
    tweets = text("""
                    SELECT "name", X.USER_ID, IMG_URL, USERNAME, TWEET_ID, TWEET, x.attachment, x.created_at, LIKED, likes FROM    
                    (SELECT T.CREATED_AT, T.attachment, T.USER_ID, T.TWEET_ID, T.TWEET, COUNT(L.USER_ID) AS LIKED, array_agg(u.username) AS likes  FROM TWEETS T
                    LEFT JOIN "like" L ON T.TWEET_ID = L.TWEET_ID
                    LEFT JOIN users u ON u.user_id = l.user_id
                    WHERE T.USER_ID = :user_id
                    GROUP BY T.TWEET_ID) X
                    JOIN USERS U ON U.USER_ID = X.USER_ID
                    ORDER BY x.created_at desc
                    """).params(user_id = user_id)
    
    result = db.engine.connect().execute(tweets).mappings().all()
    
    return [{'tweet' : t.tweet,
             'attachment' : t.attachment,
             'name' : t.name,
             'username' : t.username,
             'user_id' : t.user_id,
             'profile' : t.img_url,
             'created_at' : t.created_at,
             'liked_count' : t.liked, 
             'liked_list' : t.likes,
             'tweet_id' : t.tweet_id
             } for t in result]
    
def get_tweets_id(id):
    user = Users.query.filter_by(user_id = id).first_or_404()
    if len(user.tweet_list) <= 0:
        return {"msg" : "Haven't Post Any Tweets"}, 400
    
    return {'tweets': [{"tweet" : tweet.tweet,
            "posted_by" : tweet.user.username,
            "created_at" : tweet.created_at} for tweet in user.tweet_list]}
    
def get_tweets(username):
    user = Users.query.filter_by(username = username).first_or_404()
    
    if len(user.tweet_list) <= 0:
        return {"msg" : f"{username} Haven't Post Any Tweets"}, 400
    
    return {'tweet_count' : len(user.tweet_list),
            'tweets': [{"tweet" : tweet.tweet,
            "posted_by" : tweet.user.username,
            "created_at" : tweet.created_at} for tweet in user.tweet_list]}
    
def search_tweet(content):
    tweet = Tweet.query.filter(Tweet.tweet.ilike(f"%{content}%")).all()
    
    return [{"tweet": t.tweet,
            "posted_by" : t.user.username} 
            for t in tweet], 200

def post_tweet():
    data = request.form
    user_id = current_user.user_id
    
    if data.get('tweet') != None:
        if len(data.get('tweet')) > 280:
            return {"msg" : 'Maximum Tweet is 280 Characters'}, 400
        
        if len(data.get('tweet')) <= 0:
            return {"msg" : 'Tweet Cannot be Empty'}, 400

        t= Tweet(
            user_id = user_id,
            tweet = data.get('tweet')
            )
        db.session.add(t)
        db.session.commit()
        return {"msg" : 'Tweet Posted'} , 201

    else:
        return {"msg" : 'Tweet Cannot be Empty'}, 400
    
def post_pict():
    data = request.form
    attachment = request.files.get('attachment')
    user_id = current_user.user_id
    
    if data.get('tweet') != None:
        if len(data.get('tweet')) > 280:
            return {"msg" : 'Maximum Tweet is 280 Characters'}, 400
        
        if len(data.get('tweet')) <= 0:
            return {"msg" : 'Tweet Cannot be Empty 1'}, 400
        
        if attachment == None:
            filename = ""
    
        if attachment != None:
            filename = "tweetPict" + uuid4().hex + "." + secure_filename(attachment.filename.split(".")[-1])
            format = filename.rsplit('.', 1)[1].lower()
            
            if format not in {"gif", "jpg", "jpeg", "png", "bmp", "tiff"}:
                return {"msg" : 'File does not Support'}, 400
            
            path_img = os.path.join('tweetImg', filename)
            attachment.save(path_img)

        t= Tweet(
                user_id = user_id,
                tweet = data.get('tweet'),
                attachment = filename,
                created_at = datetime.now()
                )
        db.session.add(t)
        db.session.commit()
        return {"msg" : 'Tweet Posted'} , 200
        
    else:
        return {"msg" : 'Tweet Cannot be Empty'}, 400

def edit_tweet(tweet_id):
    data = request.form
    user_id = current_user.user_id
    tweet = Tweet.query.filter_by(tweet_id = tweet_id).first_or_404()
    
    if user_id == tweet.user_id:
        tweet.tweet = data.get('tweet')
        db.session.commit()
        return {"msg" : "Tweet Edited"}, 200
    
    return {"msg" : "Tweet Id Is Not Match"}, 400
    
def delete_tweet(tweet_id):
    user_id = current_user.user_id
    tweet = Tweet.query.filter_by(tweet_id=tweet_id, user_id=user_id).first_or_404()
    
    if user_id == tweet.user_id:
        db.session.delete(tweet)
        db.session.commit() 
        return {"msg" : f'Tweet {tweet.tweet} deleted'}, 200
    
    if tweet_id != tweet.tweet_id:
        return {"msg" : "Tweet Id Is Not Match"}, 400

def like_tweet(tweet_id):
    user = current_user.user_id
    user_id = Users.query.filter_by(user_id = user).first()
    tweet = Tweet.query.filter_by(tweet_id = tweet_id).first_or_404() 
    
    if tweet == None :
        return {"msg" : 'Invalid tweet id'}, 400
    
    found = False
    
    for i in range(len(tweet.liked)):
        if tweet.liked[i].user_id == user:
            found = True
            return {"msg" : "Already Liked"}, 200

    if found == False:   
        tweet.liked.append(user_id)
        db.session.commit()
        return {'liked_by': [user.username for user in tweet.liked]}    
        
def unlike_tweet(tweet_id):
    user = current_user.user_id
    user_id = Users.query.filter_by(user_id = user).first()
    tweet = Tweet.query.filter_by(tweet_id = tweet_id).first_or_404() 
    
    if tweet == None :
        return {"msg" : 'Invalid tweet id'}, 400
    
    found = False
    
    for i in range(len(tweet.liked)):
        if tweet.liked[i].user_id == user:
            tweet.liked.pop(i)
            db.session.commit()
            found = True
            return {"msg" : "Already Unliked"}, 200

    if found == False:   
        return {"msg" : "You Haven't Like This Tweet Yet"}, 400    
        
def most_liked():
    likes = text("""SELECT "name", X.USER_ID, IMG_URL, USERNAME, TWEET_ID, TWEET, x.attachment, x.created_at, LIKED, likes FROM    
                    (SELECT T.CREATED_AT, T.attachment, T.USER_ID, T.TWEET_ID, T.TWEET, COUNT(L.USER_ID) AS LIKED, array_agg(u.username) AS likes  FROM TWEETS T
                    LEFT JOIN "like" L ON T.TWEET_ID = L.TWEET_ID
                    LEFT JOIN users u ON u.user_id = l.user_id
                    GROUP BY T.TWEET_ID) X
                    JOIN USERS U ON U.USER_ID = X.USER_ID
                    WHERE u."status" IN ('active', 'inactive')
					ORDER BY x.liked DESC""")
    result = db.engine.connect().execute(likes).mappings().all()
    return {'result' : [dict(r) for r in result]}