from flask import request, abort, g, jsonify
from Models.modelsUsers import Users, Role, Status
from functools import wraps
from . import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, create_refresh_token
import bcrypt


# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         data = request.authorization
#         if data != None:
#             username = data.parameters['username']
#             password = data.parameters['password']
            
#             # print(username, password)
        
#             user = Users.query.filter_by(username=username).first()
#             if username == "" :
#                 abort(401, 'Enter Username')
                
#             if password == "" and len(password):
#                 abort(401, 'Enter Password')
            
#             if user != None:
#                 is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
#                 # print(is_match)
#                 if is_match == True:
#                     g.user = user
#                 else :
#                     abort(401, 'Password Incorrect')
                                
#             return f(*args, **kwargs)
#         else :
#             abort(401, 'Authorization Required')
            
#         wrap.__name__ = f.__name__
#     return wrap

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = Users.query.filter_by(username = username).first()
    print(user)
    print(username, password)
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
    
    

            
# def developer(f):
#     def wrap(*args, **kwargs):
#         if g.user.role != Role.developer:
#             abort(401, 'User Not Allowed')
            
#         return f(*args, **kwargs)
        
#     wrap.__name__ = f.__name__
#     return wrap

# # def banned(f):
#     def wrap(*args, **kwargs):
#         if g.user.status == Status.inactive:
#             g.user.status = Status.active
#             db.session.commit()
#             return f'Welcome Back {g.user.username}'
        
#         if g.user.status == Status.banned:
#             abort(401, 'This Account Has Been Suspended')
            
#         return f(*args, **kwargs)
        
#     wrap.__name__ = f.__name__
#     return wrap