from . import db
from sqlalchemy.orm import relationship
import datetime
import enum

follow = db.Table('follow',
                db.Column('follow', db.Integer, db.ForeignKey('users.user_id'), primary_key = True),
                db.Column('followed', db.Integer, db.ForeignKey('users.user_id'), primary_key = True)
                )
class Status(enum.Enum):
    active = 'User active'
    inactive = 'User inactive more than 2 months, or deactivated by themself'
    banned = 'User permanently banned'

class Role(enum.Enum):
    user = 'Common User'
    developer = 'Developer'

class Users(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now(), nullable = False)
    bio = db.Column(db.String(255))
    last_login = db.Column(db.DateTime, default = datetime.datetime.now(), nullable = False)
    role = db.Column(db.Enum(Role), default = Role.user)
    status = db.Column(db.Enum(Status), default = Status.active)
    
    
    # followed = relationship('Users', secondary = follow, backref = 'user_followed', foreign_keys='follow.followed')
    # follows = relationship('Users', secondary = follow, backref = 'user_following', foreign_keys='follow.follow')
    following_list = db.relationship('Users', 
                                secondary = follow, 
                                primaryjoin = (follow.c.follow == user_id),
                                secondaryjoin = (follow.c.followed == user_id),
                                backref = 'follower_list'
                                )
    
    tweet_list =  db.relationship('Tweet', backref = 'user', lazy = True)
    
def __repr__(self):
    return f'<user {self.user_id}'