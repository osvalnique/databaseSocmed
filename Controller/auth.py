from flask import request, json, abort
from Models.modelsUsers import Users
from functools import wraps
import bcrypt
# import jsonpickle

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.authorization
        if data != None:
            username = data.parameters['username']
            password = data.parameters['password']
            
            # print(username, password)
        
            user = Users.query.filter_by(username=username).first()
            # print(user)
            if username == "" :
                abort(401, 'Enter Username')
                
            if password == "" :
                abort(401, 'Enter Password')
            
            if user != None:
                is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
                # print(is_match)
                if is_match == True:
                    return user
                else :
                    abort(401, 'Password Incorrect')
            
            return f(*args, **kwargs)
        
        wrap.__name__ = f.__name__
    return wrap

# def developer(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         data = Users.role
#         print(data)
#         if data == 'user':
#             abort(401, 'User Not Allowed')
            
#         return f(*args, **kwargs)
        
#     wrap.__name__ = f.__name__
#     return wrap

# from functools import wraps
# from flask import abort

# def developer(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         # Assuming Users.role is a valid way to get the user's role
#         data = Users.role  # You need to define Users.role somewhere in your code
        
#         print(data)
#         if data == 'user':
#             abort(401, 'User Not Allowed')
        
#         return f(*args, **kwargs)
        
#     return wrap

             
                

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#     data = request.authorization
    
#         if not request.headers["authorization"]:
#             return redirect("login page")
#         # get user via some ORM system
#         user = User.get(request.headers["authorization"])
#         # make user available down the pipeline via flask.g
#         g.user = user
#         # finally call f. f() now haves access to g.user
#         return f(*args, **kwargs)
   
#     return wrap