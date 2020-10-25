import requests, json
from flask import request

class OfficeService:
    @staticmethod
    def get_all():
        try:
            get_offices_resp = requests.get("{}api/office/".format(request.url_root))

            if get_offices_resp.ok:
                return json.loads(get_offices_resp.text)

            return get_offices_resp.status_code

        except:
            return 500

    @staticmethod
    def post(data):
        try: 
            post_office_resp = requests.post(
                "{}api/office/".format(request.url_root),
                json= dict(
                    name = data.form.get("crtof_name_input")
                )
            )

            if post_office_resp.ok:
                return json.loads(post_office_resp.text)

            return post_office_resp.status_code

        except:
            return 500