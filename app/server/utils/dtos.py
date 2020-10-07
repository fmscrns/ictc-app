from flask_restx import Namespace, fields

class RequestDto:
    api = Namespace("request", path="/request")

    request = api.model("request", {
        "id": fields.String(),
        "no": fields.String(required=True),
        "date": fields.DateTime(dt_format="rfc822", required=True),
        "detail": fields.String(),
        "result": fields.Integer(required=True),
        "rating": fields.Integer(),
        "photo_fn": fields.String(required=True),
        "office": fields.Nested(
            api.model("office", {
                "id": fields.String(required=True, attribute="office_id"),
                "name": fields.String(attribute="office_name")
            })
        ),
        "mode": fields.Nested(
            api.model("mode", {
                "id": fields.String(required=True, attribute="mode_id"),
                "name": fields.String(attribute="mode_name")
            })
        ),
        "nature": fields.Nested(
            api.model("nature", {
                "id": fields.String(required=True, attribute="nature_id"),
                "name": fields.String(attribute="nature_name")
            })
        ),
        "technicians": fields.List(
            fields.Nested(
                api.model("technicians", {
                    "id": fields.String(required=True, attribute="technician_id"),
                    "name": fields.String(attribute="technician_name")
                })
            )
        )
    })