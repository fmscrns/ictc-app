
from app import db, client_bp, server_bp
from .client import controllers
from .server import api, create_server_bp
from .server.controllers import *
from .server import models

def establish_routes(app):
    api.add_namespace(request_ns)

    app.register_blueprint(client_bp)
    app.register_blueprint(server_bp)

    return app