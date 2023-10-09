from . import db
from sqlalchemy.orm import relationship
import datetime

like = db.Table('like',
                db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key = True),
                db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.tweet_id'), primary_key = True)
)
class Tweet(db.Model):
    __tablename__ = 'tweets'
    
    tweet_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    tweet = db.Column(db.String(280), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now(), nullable = False)
    
    liked = relationship('Users', secondary = like, lazy='subquery', backref = db.backref('tweet_liked', lazy=True))
    
def __repr__(self):
    return f'<tweet {self.tweet_id}'

# get tweet id
# get user liked the tweet
# tweet.liked.append(user)
# route liked/id tweet, method['put']

# tweet.likes=[<user 1>,<user 2>,<user 3>]

# def isUrang(id):
# 	return user.id != id
 
 
 
 
# new_likes= filter(isUrang,tweet.likes)
# tweet.likes=new_likes
# tweet_id, user_id, created_at

