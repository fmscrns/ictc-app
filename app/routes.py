from app import app, db
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, session
from app.models import *

@app.route("/", methods=["GET", "POST"])
def dashboard():
    
    return render_template("dashboard.html",
        page_title = "Dashboard",
    )

@app.route("/requests", methods=["GET", "POST"])
def requests():
    requests = []
    
    return render_template("requests.html",
        page_title="Requests",
        requests = requests
    )
