from flask import Blueprint
from flask_restx import Api

api = Api()

def create_server_bp():
    server_blueprint = Blueprint("server", __name__, url_prefix="/api")

    api.init_app(server_blueprint, add_specs=False)

    return server_blueprint