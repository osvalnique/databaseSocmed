from datetime import datetime
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
    
    if user.status == Status.banned:
        return {"msg" :'This Account is Suspended'}, 401
        
    # if user == Status.inactive:
    #         user = Status.active
    #         db.session.commit()
    #         return {"msg" : f'Welcome Back {user.username}'}
    
    else:
        user.last_login = datetime.now()
        data = {"name": user.name,
                "img_url": user.img_url,
                "username": user.username,
                "user_id": user.user_id
                }

        access_token = create_access_token(identity=user.user_id, additional_claims=data)
        refresh_token = create_refresh_token(identity=user.user_id)
        if user.role == Role.developer:
            role = "developer"   
        else:
            role = "user"
        db.session.commit()
        return jsonify(access_token=access_token,
                       refresh_token=refresh_token,
                       role= role)
    
        
def refresh_token():
    identity= get_jwt_identity()
    user = current_user
    data = {"name": user.name,
                "img_url": user.img_url,
                "username": user.username,
                "user_id": user.user_id
                }
    new_token = create_access_token(identity=identity, additional_claims=data)
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
        user = current_user.status
    
        if user == Status.banned:
            abort(401, {"msg" :'This Account is Suspended'})
            
        if user == Status.inactive:
            user = Status.active
            db.session.commit()
            return {"msg" : f'Welcome Back {user.username}'}

        return f(*args, **kwargs)
        
    wrap.__name__ = f.__name__
    return wrap
