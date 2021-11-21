"""
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///converter.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['JWT_SECRET_KEY'] = 'k#4ASfdfjo4343@$.-'
    app.config['UPLOAD_FOLDER'] = './originales'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app
"""    
