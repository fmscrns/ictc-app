import os
from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from .utils._config import config_dict
from .client import create_client_bp
from .server import create_server_bp

db = SQLAlchemy()

server_bp = create_server_bp()
client_bp = create_client_bp()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    db.init_app(app)

    return app