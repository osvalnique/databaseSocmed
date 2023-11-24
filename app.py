from flask import Flask
from Routes import blueprint
from Controller import db
from Models.modelsUsers import Users
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
 
 
def create_app():

    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ernest2210@localhost:5432/dbsocmed'

    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=6)
    jwt = JWTManager(app)
    db.init_app(app)
    
    with app.app_context():
        print("create_db")
        db.create_all()
        
    app.register_blueprint(blueprint)
    
    @jwt.user_lookup_loader
    def user_look_up(__jwt_headers,jwt_data):
        identity=jwt_data['sub']
        return Users.query.filter_by(username=identity).first()

    
    
    return app
    
