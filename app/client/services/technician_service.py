import requests, json
from flask import request

class TechnicianService:
    @staticmethod
    def get_all():
        try:
            get_technicians_resp = requests.get("{}api/technician/".format(request.url_root))

            if get_technicians_resp.ok:
                return json.loads(get_technicians_resp.text)

            return get_technicians_resp.status_code

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            post_technician_resp = requests.post(
                "{}api/technician/".format(request.url_root),
                json= dict(
                    name = data.form.get("crttc_name_input")
                )
            )

            if post_technician_resp.ok:
                return json.loads(post_technician_resp.text)

            return post_technician_resp.status_code

        except:
            return 500