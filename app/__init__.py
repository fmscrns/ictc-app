import os
from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/ictc-service-tracker"

db = SQLAlchemy(app)

client_blueprint = Blueprint("client", __name__)
server_blueprint = Blueprint("server", __name__, url_prefix="/api")

api = Api()
api.init_app(server_blueprint, add_specs=False)

from app.controllers import *

api.add_namespace(request_namespace, path="/request")

app.register_blueprint(client_blueprint)
app.register_blueprint(server_blueprint)