from flask import render_template, url_for, flash, redirect, request
from ... import client_bp
from ..forms.request_form import CreateRequestForm

@client_bp.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html",
        page_title = "Dashboard",
    )

@client_bp.route("/requests", methods=["GET", "POST"])
def requests():
    createRequestForm = CreateRequestForm()

    if request.method == "POST":
        data_txt = request.form
        data_file = request.files

        if createRequestForm.validate_on_submit():
            

            flash("Request added successfully.", "success")

            return redirect(url_for("client.requests"))

        flash("Try again.", "warning")

    return render_template("requests.html",
        page_title="Requests",
        createRequestForm = createRequestForm
    )

