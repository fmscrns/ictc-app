import requests, json
from flask import request

class NatureService:
    @staticmethod
    def get_all(pagination_no=1):
        try:
            get_natures_resp = requests.get("{}api/nature/?pagination_no={}".format(request.url_root, pagination_no))

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

    @staticmethod
    def edit(data):
        try:
            edit_nature_resp = requests.patch(
                "{}api/nature/{}".format(request.url_root, data.form.get("edtnt_id_input")),
                json= dict(
                    name = data.form.get("edtnt_name_input")
                )
            )
            
            if edit_nature_resp.ok:
                return json.loads(edit_nature_resp.text)

            return edit_nature_resp.status_code

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            delete_nature_resp = requests.delete(
                "{}api/nature/{}".format(request.url_root, data.form.get("deltnt_id_input")),
                json= dict(
                    name = data.form.get("deltnt_name_input")
                )
            )
            
            if delete_nature_resp.ok:
                return json.loads(delete_nature_resp.text)

            return delete_nature_resp.status_code

        except:
            return 500

            