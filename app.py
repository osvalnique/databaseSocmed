from flask import Flask
from Routes import blueprint
from Controller import db
from flask_jwt_extended import JWTManager
 
 
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ernest2210@localhost:5432/dbsocmed'
    
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)
    db.init_app(app)
    
    with app.app_context():
        print("create_db")
        db.create_all()
        
    app.register_blueprint(blueprint)
    
    
    return app
    
