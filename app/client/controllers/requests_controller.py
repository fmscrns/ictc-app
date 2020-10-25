from flask import render_template, url_for, flash, redirect, request, abort
from ... import client_bp
from ..forms.request_form import CreateRequestForm
from ..forms.office_form import CreateOfficeForm
from ..forms.mode_form import CreateModeForm
from ..forms.nature_form import CreateNatureForm
from ..forms.technician_form import CreateTechnicianForm
from ..services.request_service import RequestService
from ..services.office_service import OfficeService
from ..services.mode_service import ModeService
from ..services.nature_service import NatureService
from ..services.technician_service import TechnicianService
from ..utils._error_handlers import * 

@client_bp.route("/requests", methods=["GET", "POST"])
def requests():
    createRequestForm = CreateRequestForm().ready_form()
    createOfficeForm = CreateOfficeForm()
    createModeForm = CreateModeForm()
    createNatureForm = CreateNatureForm()
    createTechnicianForm = CreateTechnicianForm()

    if request.method == "POST":
        if createRequestForm.crtrq_no_input.data:
            if createRequestForm.validate_on_submit():
                post_request_resp = RequestService.post(request)

                if not isinstance(post_request_resp, int):
                    flash("Request added successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(post_request_resp)

        if createOfficeForm.crtof_name_input.data:
            if createOfficeForm.validate_on_submit():
                post_office_resp = OfficeService.post(request)

                if not isinstance(post_office_resp, int):
                    flash("Office added successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(post_office_resp)

        if createModeForm.crtmd_name_input.data:
            if createModeForm.validate_on_submit():
                post_mode_resp = ModeService.post(request)

                if not isinstance(post_mode_resp, int):
                    flash("Mode added successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(post_mode_resp)

        if createNatureForm.crtnt_name_input.data:
            if createNatureForm.validate_on_submit():
                post_nature_resp = NatureService.post(request)

                if not isinstance(post_nature_resp, int):
                    flash("Nature added successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(post_nature_resp)

        if createTechnicianForm.crttc_name_input.data:
            if createTechnicianForm.validate_on_submit():
                post_technician_resp = TechnicianService.post(request)

                if not isinstance(post_technician_resp, int):
                    flash("Technician added successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(post_technician_resp)

    return render_template("requests.html",
        page_title="Requests",
        createRequestForm = createRequestForm,
        createOfficeForm = createOfficeForm,
        createModeForm = createModeForm,
        createNatureForm = createNatureForm,
        createTechnicianForm = createTechnicianForm
    )