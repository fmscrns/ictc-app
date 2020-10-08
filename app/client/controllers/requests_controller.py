from flask import render_template, url_for, flash, redirect, request
from ... import client_bp
from ..forms.request_form import CreateRequestForm
from ..services.request_service import RequestService
from ..services.office_service import OfficeService
from ..services.mode_service import ModeService
from ..services.nature_service import NatureService
from ..services.technician_service import TechnicianService

@client_bp.route("/requests", methods=["GET", "POST"])
def requests():
    createRequestForm = CreateRequestForm()
    
    createRequestForm.office_input.choices = [(office["id"], office["name"]) for office in OfficeService.get_all()["offices"]]
    createRequestForm.mode_input.choices = [(mode["id"], mode["name"]) for mode in ModeService.get_all()["modes"]]
    createRequestForm.nature_input.choices = [(nature["id"], nature["name"]) for nature in NatureService.get_all()["natures"]]
    createRequestForm.technician_input.choices = [(technician["id"], technician["name"]) for technician in TechnicianService.get_all()["technicians"]]

    if request.method == "POST":
        data = dict(
            text = request.form,
            files = request.files
        )

        if createRequestForm.validate_on_submit():
            post_request = RequestService.post(data)

            if not isinstance(post_request, int):
                flash("Request added successfully.", "success")

                return redirect(url_for("client.requests"))

        flash("Try again.", "warning")

    return render_template("requests.html",
        page_title="Requests",
        createRequestForm = createRequestForm
    )