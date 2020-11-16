from flask_restx import Namespace, fields

class RequestDto:
    api = Namespace("request", path="/request")

    no_pattern = "([1-9]|1[012])-([1-9]|([1-9][0-9]))+"
    # date_pattern = "(\d{4}-\d{2}-\d{2} ([2][0-3]|[0-1][0-9]|[1-9]):[0-5][0-9]:([0-5][0-9]|[6][0]))"
    date_pattern = "\d{4}-\d{2}-\d{2}"
    photo_fn_pattern = "(.*/)*.+\.(png|jpg|jpeg|PNG|JPG|JPEG)"
    id_pattern = "[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"

    request = api.model("request", {
        "id": fields.String(),
        "no": fields.String(required=True, pattern=no_pattern),
        "date": fields.String(dt_format="rfc822", required=True, pattern=date_pattern),
        "detail": fields.String(),
        "result": fields.Integer(required=True, min=0, max=2),
        "rating": fields.Integer(required=True, min=0, max=5),
        "photo_fn": fields.String(required=True, pattern=photo_fn_pattern),
        "client": fields.Nested(
            api.model("client", {
                "id": fields.String(required=True, attribute="client_id", pattern=id_pattern),
                "name": fields.String(attribute="client_name")
            }), required = True
        ),
        "approach": fields.Nested(
            api.model("approach", {
                "id": fields.String(required=True, attribute="approach_id", pattern=id_pattern),
                "name": fields.String(attribute="approach_name")
            }), required = True
        ),
        "type": fields.Nested(
            api.model("type", {
                "id": fields.String(required=True, attribute="type_id", pattern=id_pattern),
                "name": fields.String(attribute="type_name")
            }), required = True
        ),
        "fixers": fields.List(
            fields.Nested(
                api.model("fixer", {
                    "id": fields.String(required=True, attribute="fixer_id", pattern=id_pattern),
                    "name": fields.String(attribute="fixer_name")
                }), required = True
            ), min_items = 1
        )
    })

class OfficeDto:
    api = Namespace("office", path="/office")

    hasText_pattern = "(.|\s)*\S(.|\s)*"

    office = api.model("office", {
        "id": fields.String(),
        "name": fields.String(required=True, pattern=hasText_pattern),
        "total_requests": fields.Integer()
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
        "name": fields.String(required=True, pattern=hasText_pattern),
        "total_requests": fields.Integer()
    })

class TechnicianDto:
    api = Namespace("technician", path="/technician")

    hasText_pattern = "(.|\s)*\S(.|\s)*"

    technician = api.model("technician", {
        "id": fields.String(),
        "name": fields.String(required=True, pattern=hasText_pattern),
        "total_requests": fields.Integer()
    })