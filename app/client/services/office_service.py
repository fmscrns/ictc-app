import requests, json
from flask import request

class OfficeService:
    @staticmethod
    def get_all(pagination_no=1):
        try:
            get_offices_resp = requests.get("{}api/office/?pagination_no={}".format(request.url_root, pagination_no))

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

    @staticmethod
    def edit(data):
        try:
            edit_office_resp = requests.patch(
                "{}api/office/{}".format(request.url_root, data.form.get("edtof_id_input")),
                json= dict(
                    name = data.form.get("edtof_name_input")
                )
            )
            
            if edit_office_resp.ok:
                return json.loads(edit_office_resp.text)

            return edit_office_resp.status_code

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            delete_office_resp = requests.delete(
                "{}api/office/{}".format(request.url_root, data.form.get("deltof_id_input")),
                json= dict(
                    name = data.form.get("deltof_name_input")
                )
            )
            
            if delete_office_resp.ok:
                return json.loads(delete_office_resp.text)

            return delete_office_resp.status_code

        except:
            return 500