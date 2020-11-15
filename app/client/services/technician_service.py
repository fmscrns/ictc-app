import requests, json
from flask import request

class TechnicianService:
    @staticmethod
    def get_all(pagination_no=1):
        try:
            get_technicians_resp = requests.get("{}api/technician/?pagination_no={}".format(request.url_root, pagination_no))

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

    @staticmethod
    def edit(data):
        try:
            edit_technician_resp = requests.patch(
                "{}api/technician/{}".format(request.url_root, data.form.get("edttc_id_input")),
                json= dict(
                    name = data.form.get("edttc_name_input")
                )
            )
            
            if edit_technician_resp.ok:
                return json.loads(edit_technician_resp.text)

            return edit_technician_resp.status_code

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            delete_technician_resp = requests.delete(
                "{}api/technician/{}".format(request.url_root, data.form.get("delttc_id_input")),
                json= dict(
                    name = data.form.get("delttc_name_input")
                )
            )
            
            if delete_technician_resp.ok:
                return json.loads(delete_technician_resp.text)

            return delete_technician_resp.status_code

        except:
            return 500