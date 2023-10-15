from flask import request, abort, g
from Models.modelsUsers import Users, Role, Status
from functools import wraps
from . import db
import bcrypt


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.authorization
        if data != None:
            username = data.parameters['username']
            password = data.parameters['password']
            
            # print(username, password)
        
            user = Users.query.filter_by(username=username).first()
            if username == "" :
                abort(401, 'Enter Username')
                
            if password == "" and len(password):
                abort(401, 'Enter Password')
            
            if user != None:
                is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
                # print(is_match)
                if is_match == True:
                    g.user = user
                else :
                    abort(401, 'Password Incorrect')
                                
            return f(*args, **kwargs)
        else :
            abort(401, 'Authorization Required')
            
        wrap.__name__ = f.__name__
    return wrap

def developer(f):
    def wrap(*args, **kwargs):
        if g.user.role != Role.developer:
            abort(401, 'User Not Allowed')
            
        return f(*args, **kwargs)
        
    wrap.__name__ = f.__name__
    return wrap

def banned(f):
    def wrap(*args, **kwargs):
        if g.user.status == Status.inactive:
            g.user.status = Status.active
            db.session.commit()
            return f'Welcome Back {g.user.username}'
        
        if g.user.status == Status.banned:
            abort(401, 'This Account Has Been Suspended')
            
        return f(*args, **kwargs)
        
    wrap.__name__ = f.__name__
    return wrap
