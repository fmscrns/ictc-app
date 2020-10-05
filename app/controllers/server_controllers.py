from flask import render_template, jsonify
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import *

request_namespace = Namespace("request")

request_dto = request_namespace.model("request", {
    "id": fields.String(),
    "no": fields.String(),
    "date": fields.DateTime(dt_format="rfc822"),
    "detail": fields.String(),
    "result": fields.Integer(),
    "rating": fields.Integer(),
    "photo_fn": fields.String(),
    "office": fields.Nested(
        request_namespace.model("office", {
            "id": fields.String(attribute="office_id"),
            "name": fields.String(attribute="office_name")
        })
    ),
    "mode": fields.Nested(
        request_namespace.model("mode", {
            "id": fields.String(attribute="mode_id"),
            "name": fields.String(attribute="mode_name")
        })
    ),
    "nature": fields.Nested(
        request_namespace.model("nature", {
            "id": fields.String(attribute="nature_id"),
            "name": fields.String(attribute="nature_name")
        })
    ),
    "technicians": fields.List(
        fields.Nested(
            request_namespace.model("technicians", {
                "id": fields.String(attribute="technician_id"),
                "name": fields.String(attribute="technician_name")
            })
        )
    )
})



@request_namespace.route("/")
class Request(Resource):
    @request_namespace.marshal_list_with(request_dto, envelope="requests")
    def get(self):
        return [
            dict(
                id = request[0],
                no = request[1],
                date = request[2],
                detail = request[3],
                result = request[4],
                rating = request[5],
                photo_fn = request[6],
                office = dict(
                    office_id = request[7],
                    office_name = request[8],
                ),
                mode = dict(
                    mode_id = request[9],
                    mode_name = request[10]
                ),
                nature = dict(
                    nature_id = request[11],
                    nature_name = request[12]
                ),
                technicians = [
                    dict(
                        technician_id = technician[0],
                        technician_name = technician[1]
                    ) for technician in db.session.query(
                        TechnicianModel.public_id,
                        TechnicianModel.name
                    ).filter(
                        TechnicianModel.public_id == RepairModel.technician_fixer_id,
                        RepairModel.request_task_id == request[0]
                    ).all()
                ]
            ) for request in db.session.query(
                RequestModel.public_id,
                RequestModel.no,
                RequestModel.date,
                RequestModel.detail,
                RequestModel.result,
                RequestModel.rating,
                RequestModel.photo_fn,
                OfficeModel.public_id,
                OfficeModel.name,
                ModeModel.public_id,
                ModeModel.name,
                NatureModel.public_id,
                NatureModel.name
            ).filter(
                RequestModel.office_client_id == OfficeModel.public_id
            ).filter(
                RequestModel.mode_approach_id == ModeModel.public_id
            ).filter(
                RequestModel.nature_type_id == NatureModel.public_id
            ).all()
        ]