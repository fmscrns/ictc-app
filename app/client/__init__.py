from flask import Blueprint

def create_client_bp():
    client_blueprint = Blueprint("client", __name__, template_folder="templates", static_url_path="static")
    
    return client_blueprint