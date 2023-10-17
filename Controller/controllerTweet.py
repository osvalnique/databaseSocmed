from sqlalchemy import text
from Models import Tweet, Users
from flask import request
from . import db

# post tweet DONE
# edit tweet DONE
# delete tweet DONE
# read tweet DONE
# read others tweet DONE
# like tweet DONE
# unlike tweet DONE
# search tweet DONE

# most liked tweet

# delete others tweet * DONE


def get_all():
    tweets = Tweet.query.all()
    
    return [{"tweet" : tweet.tweet,
             "posted_by" : tweet.user.username,
             "created_at" : tweet.created_at} for tweet in tweets]

def get_tweet(id):
    tweet = Tweet.query.filter_by(tweet_id = id).first_or_404()
    
    return {"tweet" : tweet.tweet,
            "posted_by" : tweet.user.username,
            "created_at" : tweet.created_at} 
    
def get_tweets(username):
    user = Users.query.filter_by(username = username).first_or_404()
    if len(user.tweet_list) <= 0:
        return f"{username} Haven't Post Any Tweets"
    
    return {'tweets': [{"tweet" : tweet.tweet,
            "posted_by" : tweet.user.username,
            "created_at" : tweet.created_at} for tweet in user.tweet_list]}
    
def search_tweet(content):
    tweet = Tweet.query.filter(Tweet.tweet.ilike(f"%{content}%")).all()
    
    return [{"tweet": t.tweet,
            "posted_by" : t.user.username} 
            for t in tweet], 200

def post_tweet():
    tweet = request.get_json()
    
    t= Tweet(
        user_id = tweet['user_id'],
        tweet = tweet['tweet']
        )
    db.session.add(t)
    db.session.commit()
    return 'Tweet Posted', 200

def edit_tweet(id):
    data = request.get_json()
    tweet = Tweet.query.filter_by(tweet_id = id).first_or_404()
    
    tweet.tweet = data['tweet']
    db.session.commit()
    return "Tweet Edited", 200
    
def delete_tweet(id):
    tweet = Tweet.query.filter_by(tweet_id=id).first_or_404() 
    return f'Tweet "{tweet.tweet}" deleted'

def like_tweet(id):
    data = request.get_json()
    if 'user_id' not in data:
        return 'Please Input user_id', 400
        
    tweet = Tweet.query.filter_by(tweet_id=id).first_or_404() 
    user = Users.query.filter_by(user_id=data['user_id']).first()
    if user == None :
        return 'Invalid user_id'
    found = False
    
    for i in range(len(tweet.liked)):
        if tweet.liked[i].user_id == user.user_id:
            tweet.liked.pop(i)
            found = True
            break
    if found == False:   
        tweet.liked.append(user)
        
    db.session.commit()
    return {'liked_by': [user.username for user in tweet.liked]}

def most_liked():
    likes = text('SELECT t.tweet_id, username, tweet, x.likes\
        FROM (SELECT l.tweet_id, COUNT(l.tweet_id) likes \
        FROM "like" l GROUP BY l.tweet_id) x \
        JOIN TWEETS T ON t.TWEET_ID = x.TWEET_ID \
        JOIN USERS U ON t.USER_ID = u.USER_ID\
        ORDER BY x.likes DESC;')
    result = db.engine.connect().execute(likes).mappings().all()
    return {'results' : [dict(r) for r in result]}