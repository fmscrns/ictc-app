from flask import render_template, url_for, flash, redirect, request
from ... import client_bp

@client_bp.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html",
        page_title = "Dashboard",
    )