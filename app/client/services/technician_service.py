import requests, json
from flask import request

class TechnicianService:
    @staticmethod
    def get_all():
        api_resp = requests.get("{}api/technician/".format(request.url_root))

        if api_resp.ok:
            return json.loads(api_resp.text)