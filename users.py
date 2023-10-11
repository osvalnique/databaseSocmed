from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from authorization import auth
from models import Peminjaman, Users, db
from route import blueprint
import bcrypt
    
#API get Users
@blueprint.route('/users')
def get_users():
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    return jsonify([
        {'user_id': user.user_id,
         'username': user.username,
         'password':user.password,
         'admin' : user.admin}
        for user in Users.query.all()
        ])
    
#API get Users by ID
#API post Users
@blueprint.route('/users', methods=['POST'])
def add_users():
    data = request.get_json()
    # users = auth()
    # if users is None:
    #     return "Access Denied", 401
    
    data['password'] = str(data['password']).encode('utf-8')
    hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
    hashed = hashed.decode('utf-8')
    
    user = Users(
        username = data['username'],
        password = hashed,
        admin = data['admin']
    )
    db.session.add(user)
    db.session.commit()
    return {'user' : 'Berhasil Ditambahkan'}

#API put Users
@blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = auth()
    data = request.get_json()
    users = Users.query.filter_by(user_id=id).first_or_404()
    if users is None:
        return "Access Denied", 401
    
    if users.username is not user.username:
        print(users.username)
        return 'Username is not Match'
    
    if users.admin == False and data['admin'] == True:
        return 'Only Admin is Allowed'
    
    if users.username != data['username']:
        check = Users.query.filter_by(username=data['username']).first()
        if check != None:
            return 'Username Sudah Dipakai', 400
        
        users.username = data['username']
    
    data['password'] = str(data['password']).encode('utf-8')
    hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
    users.password = hashed

    # users.admin = data['admin']
    db.session.commit()
    
    return jsonify([{'user_id': users.user_id,
         'username': users.username,
         'password':users.password,
         'admin' : users.admin}
    ])
    
#API delete Users
@blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_users(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    data = Users.query.filter_by(user_id=id).first_or_404()
    db.session.delete(data)
    db.session.commit()
    return {'user': 'Berhasil Dihapus'}
