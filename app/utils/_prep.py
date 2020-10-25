
from .. import db, server_bp, client_bp
from ..server import api, create_server_bp
from ..server.controllers import *
from ..server import models
from ..client import controllers

def establish_routes(app):
    api.add_namespace(request_ns)
    api.add_namespace(office_ns)
    api.add_namespace(mode_ns)
    api.add_namespace(nature_ns)
    api.add_namespace(technician_ns)

    app.register_blueprint(server_bp)
    app.register_blueprint(client_bp)

    return app