from flask import request, abort, g, jsonify
from Models.modelsUsers import Users, Role, Status
from functools import wraps
from . import db
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity, jwt_required, JWTManager, create_refresh_token
import bcrypt


def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = Users.query.filter_by(username = username).first()

    if user == None :
        return {"msg" : "Username Is Not Registered"}, 401
    
    is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if is_match == False:
        return {"msg" : "Password Incorrect"}, 401
    
    else:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return jsonify(access_token=access_token,
                       refresh_token=refresh_token)
        
def refresh_token():
    identity= get_jwt_identity()
    new_token = create_access_token(identity=identity)
    return {"access_token" : new_token}
    
            
def developer(f):
    def wrap(*args, **kwargs):
        if current_user.role != Role.developer:
            abort(401, {"msg" : 'User Not Allowed'})
            
        return f(*args, **kwargs)
        
    wrap.__name__ = f.__name__
    return wrap

def banned(f):
    def wrap(*args, **kwargs):
        data = request.get_json()
        user = Users.query.filter_by(username = data['username']).first()
    
        if user.status == Status.banned:
            abort(401, {"msg" :'This Account is Suspended'})
            
        if user.status == Status.inactive:
            user.status = Status.active
            db.session.commit()
            return {"msg" : f'Welcome Back {user.username}'}

        return f(*args, **kwargs)
        
    wrap.__name__ = f.__name__
    return wrap
