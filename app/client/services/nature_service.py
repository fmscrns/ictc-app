import requests, json
from flask import request

class NatureService:
    @staticmethod
    def get_all():
        api_resp = requests.get("{}api/nature/".format(request.url_root))

        if api_resp.ok:
            return json.loads(api_resp.text)