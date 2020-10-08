import requests, json, uuid
from flask import request
from ..utils._helpers import save_new_photo

class RequestService:
    @staticmethod
    def post(data):
        photo_fn = save_new_photo(data["file"].get("photo_fn_input"))

        api_resp = requests.post(
            "{}api/request/".format(request.url_root),
            json= dict(
                no = data["text"].get("no_input"),
                date = data["text"].get("date_input"),
                detail = data["text"].get("detail_input"),
                result = data["text"].get("result_input", type=int),
                rating = data["text"].get("rating_input", type=int),
                photo_fn = photo_fn,
                office_id = data["text"].get("office_input"),
                mode_id = data["text"].get("mode_input"),
                nature_id = data["text"].get("nature_input")
            )
        )

        if api_resp.ok:
            return json.loads(api_resp.text)