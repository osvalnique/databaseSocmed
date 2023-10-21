from flask import g, request, jsonify
from Models import Users, db
from Controller import controllerUsers, auth
from . import blueprint
from flask_jwt_extended import jwt_required, current_user
import bcrypt


@blueprint.route("/login", methods=["POST"])
def login():
    login = auth.login()
    return login

@blueprint.route("/refresh")
@jwt_required(refresh = True)
def refresh():
    refresh = auth.refresh_token()
    return refresh

@blueprint.route("/user/create_users", methods = ['POST'])
def create_users():
    users = controllerUsers.create_users()
    
    return users

@blueprint.route("/user/get_users")
@jwt_required()
@auth.developer
def get_users():
    users = controllerUsers.get_all()
    
    return users

@blueprint.route("/user/<string:username>")
@jwt_required()
@auth.banned
def get_username(username):
    users = controllerUsers.get_username(username.lower())
    
    return users

@blueprint.route("/user/<uuid:id>")
@jwt_required()
@auth.banned
def get_user(id):
    users = controllerUsers.get_user(id)
    
    return users

@blueprint.route("/user/update", methods = ['PUT'])
@jwt_required()
@auth.banned
def update_user():
    users = controllerUsers.update_user()
    
    return users

@blueprint.route("/user/update/image", methods = ['PUT'])
@jwt_required()
@auth.banned
def update_image():
    users = controllerUsers.update_image()
    
    return users

@blueprint.route("/user/follow/<uuid:followed_id>", methods = ['PUT'])
@jwt_required()
@auth.banned
def follow(followed_id):
    users = controllerUsers.follow(followed_id)
    
    return users

@blueprint.route("/user/unfollow/<uuid:followed_id>", methods = ['PUT'])
@jwt_required()
@auth.banned
def unfollow(followed_id):
    users = controllerUsers.unfollow(followed_id)
    
    return users

@blueprint.route("/user/deactivate", methods = ['PUT'])
@jwt_required()
def deactivate_user():
    users = controllerUsers.deactivate_user()
    
    return users

@blueprint.route("/user/activate", methods = ['PUT'])
@jwt_required()
@auth.banned
def activate_user():
    users = controllerUsers.activate_user()
    
    return users

@blueprint.route("/user/ban/<uuid:id>", methods = ['PUT'])
@jwt_required()
@auth.developer
def ban_user(id):
    users = controllerUsers.ban_user(id)
    
    return users

@blueprint.route("/user/unban/<uuid:id>", methods = ['PUT'])
@jwt_required()
@auth.banned
def unban_user(id):
    users = controllerUsers.unban_user(id)
    
    return users

@blueprint.route("/user/last_login")
@jwt_required()
@auth.developer
def get_last_login():
    users = controllerUsers.get_last_login()
    
    return users

@blueprint.route("/user/most_followers")
@jwt_required()
def most_followers():
    users = controllerUsers.most_followers()
    
    return users

