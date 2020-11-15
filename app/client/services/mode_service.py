import requests, json
from flask import request

class ModeService:
    @staticmethod
    def get_all(pagination_no=1):
        try:
            get_modes_resp = requests.get("{}api/mode/?pagination_no={}".format(request.url_root, pagination_no))

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

    @staticmethod
    def edit(data):
        try:
            edit_mode_resp = requests.patch(
                "{}api/mode/{}".format(request.url_root, data.form.get("edtmd_id_input")),
                json= dict(
                    name = data.form.get("edtmd_name_input")
                )
            )
            
            if edit_mode_resp.ok:
                return json.loads(edit_mode_resp.text)

            return edit_mode_resp.status_code

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            delete_mode_resp = requests.delete(
                "{}api/mode/{}".format(request.url_root, data.form.get("deltmd_id_input")),
                json= dict(
                    name = data.form.get("deltmd_name_input")
                )
            )
            
            if delete_mode_resp.ok:
                return json.loads(delete_mode_resp.text)

            return delete_mode_resp.status_code

        except:
            return 500