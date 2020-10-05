import os, uuid
from app import app, client_blueprint, db
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, session
from PIL import Image
from app.models import *
from app.forms.request_form import CreateRequestForm

@client_blueprint.route("/", methods=["GET", "POST"])
def dashboard():
    
    return render_template("dashboard.html",
        page_title = "Dashboard",
    )

@client_blueprint.route("/requests", methods=["GET", "POST"])
def requests():
    createRequestForm = CreateRequestForm()

    if request.method == "POST":
        data_txt = request.form
        data_file = request.files

        if createRequestForm.validate_on_submit():
            req_pid = str(uuid.uuid4())

            filename = str(uuid.uuid4())
            _, f_ext = os.path.splitext(data_file.get("photo_fn_input").filename)
            picture_fn = filename + f_ext
            picture_path = os.path.join(app.root_path,'static/images', picture_fn)
            output_size = (500, 500)
            i = Image.open(data_file.get("photo_fn_input"))
            i.thumbnail(output_size)
            i.save(picture_path)

            new_request = RequestModel(
                public_id = req_pid,
                no = data_txt.get("no_input"),
                date = data_txt.get("date_input"),
                detail = data_txt.get("detail_input"),
                result = data_txt.get("result_input"),
                rating = data_txt.get("rating_input"),
                photo_fn = picture_fn,
                office_client_id = data_txt.get("office_input"),
                mode_approach_id = data_txt.get("mode_input"),
                nature_type_id = data_txt.get("nature_input")
            )

            db.session.add(new_request)

            for technician_id in data_txt.getlist("technician_input"):
                print(technician_id)
                rep_pid = str(uuid.uuid4())

                new_repair = RepairModel(
                    public_id = rep_pid,
                    technician_fixer_id = technician_id,
                    request_task_id = req_pid
                )

                db.session.add(new_repair)

            db.session.commit()

            flash("Request added successfully.", "success")

            return redirect(url_for("client.requests"))

        flash("Try again.", "warning")

    return render_template("requests.html",
        page_title="Requests",
        createRequestForm = createRequestForm
    )

