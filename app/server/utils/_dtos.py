from flask_restx import Namespace, fields

class RequestDto:
    api = Namespace("request", path="/request")

    no_pattern = "([1-9]|1[012])-([1-9]|([1-9][0-9]))+"
    date_pattern = "(\d{4}-\d{2}-\d{2} ([2][0-3]|[0-1][0-9]|[1-9]):[0-5][0-9]:([0-5][0-9]|[6][0]))"
    photo_fn_pattern = "(.*/)*.+\.(png|jpg|jpeg|PNG|JPG|JPEG)"
    id_pattern = "[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"

    request = api.model("request", {
        "id": fields.String(),
        "no": fields.String(required=True, pattern=no_pattern),
        "date": fields.String(dt_format="rfc822", required=True, pattern=date_pattern),
        "detail": fields.String(),
        "result": fields.Integer(required=True, min=0, max=2),
        "rating": fields.Integer(),
        "photo_fn": fields.String(required=True, pattern=photo_fn_pattern),
        "office": fields.Nested(
            api.model("office", {
                "id": fields.String(required=True, attribute="office_id", pattern=id_pattern),
                "name": fields.String(attribute="office_name")
            }), required = True
        ),
        "mode": fields.Nested(
            api.model("mode", {
                "id": fields.String(required=True, attribute="mode_id", pattern=id_pattern),
                "name": fields.String(attribute="mode_name")
            }), required = True
        ),
        "nature": fields.Nested(
            api.model("nature", {
                "id": fields.String(required=True, attribute="nature_id", pattern=id_pattern),
                "name": fields.String(attribute="nature_name")
            }), required = True
        ),
        "technicians": fields.List(
            fields.Nested(
                api.model("technicians", {
                    "id": fields.String(required=True, attribute="technician_id", pattern=id_pattern),
                    "name": fields.String(attribute="technician_name")
                })
            ), required = True
        )
    })

class OfficeDto:
    api = Namespace("office", path="/office")

    hasText_pattern = "(.|\s)*\S(.|\s)*"

    office = api.model("office", {
        "id": fields.String(),
        "name": fields.String(required=True, pattern=hasText_pattern)
    })

class ModeDto:
    api = Namespace("mode", path="/mode")

    hasText_pattern = "(.|\s)*\S(.|\s)*"

    mode = api.model("mode", {
        "id": fields.String(),
        "name": fields.String(required=True, pattern=hasText_pattern)
    })

class NatureDto:
    api = Namespace("nature", path="/nature")

    hasText_pattern = "(.|\s)*\S(.|\s)*"

    nature = api.model("nature", {
        "id": fields.String(),
        "name": fields.String(required=True, pattern=hasText_pattern)
    })

class TechnicianDto:
    api = Namespace("technician", path="/technician")

    hasText_pattern = "(.|\s)*\S(.|\s)*"

    technician = api.model("technician", {
        "id": fields.String(),
        "name": fields.String(required=True, pattern=hasText_pattern)
    })