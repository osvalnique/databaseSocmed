from . import blueprint
from Models import Users, db
from Controller import controllerUsers
from Controller.auth import login_required, developer
import bcrypt


@blueprint.route("/users")
@login_required
# @developer

def get_users():
    users = controllerUsers.get_all()
    
    return users

@blueprint.route("/users/<int:id>")
def get_user(id):
    users = controllerUsers.get_user(id)
    
    return users

@blueprint.route("/users_last_login")
def get_last_login():
    users = controllerUsers.get_last_login()
    
    return users

@blueprint.route("/users/<string:username>")
def get_profile(username):
    users = controllerUsers.get_profile(username.lower())
    
    return users

@blueprint.route("/create_users", methods = ['POST'])
def create_users():
    users = controllerUsers.create_users()
    
    return users

@blueprint.route("/follow_user", methods = ['PUT'])
def follow():
    users = controllerUsers.follow()
    
    return users

@blueprint.route("/deactivate_user/<int:id>", methods = ['PUT'])
def deactivate_user(id):
    users = controllerUsers.deactivate_user(id)
    
    return users

@blueprint.route("/update_user/<int:id>", methods = ['PUT'])
@login_required

def update_user(id):
    users = controllerUsers.update_user(id)
    
    return users

@blueprint.route("/ban_user/<int:id>", methods = ['PUT'])
def ban_user(id):
    users = controllerUsers.ban_user(id)
    
    return users