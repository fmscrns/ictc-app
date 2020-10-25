import requests, json
from flask import request

class ModeService:
    @staticmethod
    def get_all():
        try:
            get_modes_resp = requests.get("{}api/mode/".format(request.url_root))

            if get_modes_resp.ok:
                return json.loads(get_modes_resp.text)

            return get_modes_resp.status_code

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            post_mode_resp = requests.post(
                "{}api/mode/".format(request.url_root),
                json= dict(
                    name = data.form.get("crtmd_name_input")
                )
            )

            if post_mode_resp.ok:
                return json.loads(post_mode_resp.text)

            return api_resp.status_code   

        except:
            return 500