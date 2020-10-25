import requests, json
from flask import request

class NatureService:
    @staticmethod
    def get_all():
        try:
            get_natures_resp = requests.get("{}api/nature/".format(request.url_root))

            if get_natures_resp.ok:
                return json.loads(get_natures_resp.text)

            return get_natures_resp.status_code

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            post_nature_resp = requests.post(
                "{}api/nature/".format(request.url_root),
                json= dict(
                    name = data.form.get("crtnt_name_input")
                )
            )

            if post_nature_resp.ok:
                return json.loads(post_nature_resp.text)

            return post_nature_resp.status_code

        except:
            return 500

            