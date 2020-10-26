from flask import url_for, flash, redirect
from ... import client_bp

@client_bp.errorhandler(400)
def bad_request(e):
    flash(e.description, "danger")
    return redirect(url_for("client.requests"))

@client_bp.errorhandler(404)
def resource_not_found(e):
    flash(e.description, "danger")
    return redirect(url_for("client.requests"))

@client_bp.errorhandler(500)
def server_error(e):
    flash(e.description, "danger")
    return redirect(url_for("client.requests"))