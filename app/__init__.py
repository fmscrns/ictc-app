import os
from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from ._config import config_dict
from .client import create_client_bp
from .server import create_server_bp

db = SQLAlchemy()

client_bp = create_client_bp()
server_bp = create_server_bp()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    db.init_app(app)

    return app