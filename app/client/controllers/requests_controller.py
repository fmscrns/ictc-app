from flask import render_template, url_for, flash, redirect, request, abort
from ... import client_bp
from ..forms.request_form import CreateRequestForm
from ..forms.office_form import *
from ..forms.mode_form import *
from ..forms.nature_form import *
from ..forms.technician_form import *
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

    editOfficeForm = EditOfficeForm()
    editModeForm = EditModeForm()
    editNatureForm = EditNatureForm()
    editTechnicianForm = EditTechnicianForm()

    deleteOfficeForm = DeleteOfficeForm()
    deleteModeForm = DeleteModeForm()
    deleteNatureForm = DeleteNatureForm()
    deleteTechnicianForm = DeleteTechnicianForm()

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

        if editOfficeForm.edtof_id_input.data:
            if editOfficeForm.validate_on_submit():
                edit_office_resp = OfficeService.edit(request)

                if edit_office_resp == 200:
                    flash("Office edited successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(edit_office_resp)

        if editModeForm.edtmd_id_input.data:
            if editModeForm.validate_on_submit():
                edit_mode_resp = ModeService.edit(request)

                if edit_mode_resp == 200:
                    flash("Mode edited successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(edit_mode_resp)
        
        if editNatureForm.edtnt_id_input.data:
            if editNatureForm.validate_on_submit():
                edit_nature_resp = NatureService.edit(request)

                if edit_nature_resp == 200:
                    flash("Nature edited successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(edit_nature_resp)

        if editTechnicianForm.edttc_id_input.data:
            if editTechnicianForm.validate_on_submit():
                edit_technician_resp = TechnicianService.edit(request)

                if edit_technician_resp == 200:
                    flash("Technician edited successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(edit_technician_resp)

        if deleteOfficeForm.deltof_id_input.data:
            if deleteOfficeForm.validate_on_submit():
                delete_office_resp = OfficeService.delete(request)

                if delete_office_resp == 200:
                    flash("Office deleted successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(delete_office_resp)

        if deleteModeForm.deltmd_id_input.data:
            if deleteModeForm.validate_on_submit():
                delete_mode_resp = ModeService.delete(request)

                if delete_mode_resp == 200:
                    flash("Mode deleted successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(delete_mode_resp)
        
        if deleteNatureForm.deltnt_id_input.data:
            if deleteNatureForm.validate_on_submit():
                delete_nature_resp = NatureService.delete(request)

                if delete_nature_resp == 200:
                    flash("Nature deleted successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(delete_nature_resp)

        if deleteTechnicianForm.delttc_id_input.data:
            if deleteTechnicianForm.validate_on_submit():
                delete_technician_resp = TechnicianService.delete(request)

                if delete_technician_resp == 200:
                    flash("Technician deleted successfully.", "success")

                    return redirect(url_for("client.requests"))

                abort(delete_technician_resp)

    return render_template("requests.html",
        page_title="Requests",
        createRequestForm = createRequestForm,
        createOfficeForm = createOfficeForm,
        createModeForm = createModeForm,
        createNatureForm = createNatureForm,
        createTechnicianForm = createTechnicianForm,
        editOfficeForm = editOfficeForm,
        editModeForm = editModeForm,
        editNatureForm = editNatureForm,
        editTechnicianForm = editTechnicianForm,
        deleteOfficeForm = deleteOfficeForm,
        deleteModeForm = deleteModeForm,
        deleteNatureForm = deleteNatureForm,
        deleteTechnicianForm = deleteTechnicianForm
    )