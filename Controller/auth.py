from flask import request, abort
from Models.modelsUsers import Users
import bcrypt

def auth():
    data = request.authorization
    if data != None:
        username = data.parameters['username']
        password = data.parameters['password']
        
        print(username, password)
    
        user = Users().query.filter_by(username=username).first()
        # print(user)
        if username == "" :
            abort(401, 'Enter Username')
            
        if password == "" :
            abort(401, 'Enter Password')
        
        if user != None:
            is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
            if is_match == True:
                return user
            else :
                abort(401, 'Password Incorrect')