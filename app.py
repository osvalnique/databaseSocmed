from flask import Flask
from Routes import blueprint
from Controller import db
 
 
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ernest2210@localhost:5432/dbsocmed'
    db.init_app(app)
    
    app.register_blueprint(blueprint)
    
    return app
    
