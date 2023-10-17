from flask import g, request, jsonify
from . import blueprint
from Models import Users, db
from Controller import controllerUsers, auth
from flask_jwt_extended import jwt_required
# from Controller.auth import login_required, developer, banned
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

@blueprint.route("/users")
@jwt_required()
# @login_required
# @developer
# @banned
def get_users():
    users = controllerUsers.get_all()
    
    return users

@blueprint.route("/users/<uuid:id>")
# @login_required
# @developer
# @banned
def get_user(id):
    users = controllerUsers.get_user(id)
    
    return users

@blueprint.route("/users_last_login")
# @login_required
# @developer
# @banned
def get_last_login():
    users = controllerUsers.get_last_login()
    
    return users

@blueprint.route("/users/<string:username>")
# @login_required
# @developer
# @banned
def get_username(username):
    users = controllerUsers.get_username(username.lower())
    
    return users

@blueprint.route("/create_users", methods = ['POST'])
# @login_required
# @developer
# @banned
def create_users():
    users = controllerUsers.create_users()
    
    return users

@blueprint.route("/follow_user", methods = ['PUT'])
# @login_required
# @developer
# @banned
def follow():
    users = controllerUsers.follow()
    
    return users

# @blueprint.route("/get_followers/<int:id>")
# def get_followers(id):
#     users = controllerUsers.get_followers(id)
    
    # return users

@blueprint.route("/deactivate_user/<int:id>", methods = ['PUT'])
# @login_required
# @developer
# @banned
def deactivate_user(id):
    users = controllerUsers.deactivate_user(id)
    
    return users

@blueprint.route("/update_user/<int:id>", methods = ['PUT'])
# @login_required
# @developer
# @banned
def update_user(id):
    users = controllerUsers.update_user(id)
    
    return users

@blueprint.route("/ban_user/<int:id>", methods = ['PUT'])
# @login_required
# @developer
# @banned
def ban_user(id):
    users = controllerUsers.ban_user(id)
    
    return users

@blueprint.route("/most_followers")
# @login_required
# @developer
# @banned
def most_followers():
    users = controllerUsers.most_followers()
    return users

@blueprint.route("/following_tweets")
# @login_required

def get_following_tweets():
    user_id = g.user
    users = controllerUsers.get_following_tweets(user_id)
    return users
