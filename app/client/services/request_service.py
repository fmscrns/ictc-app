import os, uuid, requests, json
from flask import current_app, request
from PIL import Image

class RequestService:
    @staticmethod
    def get_all(pagination_no=1):
        try:
            get_requests_resp = requests.get("{}api/request/pagination_no={}".format(request.url_root, pagination_no))

            if get_requests_resp.ok:
                return json.loads(get_requests_resp.text)

            return get_requests_resp.status_code

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            photo_file = data.files.get("crtrq_photo_fn_input")
            
            filename = str(uuid.uuid4())
        
            _, f_ext = os.path.splitext(photo_file.filename)
            photo_fn = filename + f_ext

            photo_path = os.path.join(current_app.root_path, "static/images", photo_fn)

            i = Image.open(photo_file)
            i.thumbnail((600, 600))
            i.save(photo_path)

            post_request_resp = requests.post(
                "{}api/request/".format(request.url_root),
                json= dict(
                    no = data.form.get("crtrq_no_input"),
                    date = data.form.get("crtrq_date_input"),
                    detail = data.form.get("crtrq_detail_input"),
                    result = data.form.get("crtrq_result_input", type=int),
                    rating = data.form.get("crtrq_rating_input", type=int),
                    photo_fn = photo_fn,
                    client = dict(
                        id = data.form.get("crtrq_office_input")
                    ),
                    approach = dict(
                        id = data.form.get("crtrq_mode_input")
                    ),
                    type = dict(
                        id = data.form.get("crtrq_nature_input")
                    ),
                    fixers = [
                        dict(
                            id = technician_id
                        )
                        for technician_id in data.form.getlist("crtrq_technician_input")
                    ]
                )
            )

            if post_request_resp.ok:
                return json.loads(post_request_resp.text)

            return post_request_resp.status_code

        except:
            return 500