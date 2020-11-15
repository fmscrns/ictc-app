import datetime
from flask import render_template, url_for, flash, redirect, request
from ... import client_bp
from ..services.request_service import RequestService
from ..services.technician_service import TechnicianService

@client_bp.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html",
        page_title = "Dashboard",
        current_date = "{}".format(datetime.datetime.utcnow().strftime("%B %d, %Y")),
        request_count = 2,
        technician_count = 2
    )