from click import UUID
from . import db
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy import UUID
import datetime

like = db.Table('like',
                db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key = True),
                db.Column('tweet_id', UUID(as_uuid=True), db.ForeignKey('tweets.tweet_id'), primary_key = True)
)
class Tweet(db.Model):
    __tablename__ = 'tweets'
    
    tweet_id = db.Column(UUID(as_uuid=True) , primary_key = True, default = uuid4)
    user_id = db.Column(UUID(as_uuid = True), db.ForeignKey('users.user_id'), nullable = False)
    tweet = db.Column(db.String(280), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now(), nullable = False)
    attachment = db.Column(db.String)
    
    liked = relationship('Users', secondary = like, lazy='subquery', backref = db.backref('tweet_liked', lazy=True))
    
    
def __repr__(self):
    return f'<tweet {self.tweet_id}'


