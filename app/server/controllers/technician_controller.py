from flask import request
from flask_restx import Resource
from ..services.technician_service import TechnicianService
from ..utils._dtos import TechnicianDto

api = TechnicianDto.api
_technician = TechnicianDto.technician

@api.route("/")
class TechnicianList(Resource):
    @api.marshal_list_with(_technician, envelope="technicians")
    def get(self):
        pagination_no = request.args.get("pagination_no", 1, int)

        get_technicians = TechnicianService.get_all(pagination_no)

        if not isinstance(get_technicians, int):
            return get_technicians

        api.abort(get_technicians)

    @api.expect(_technician, validate=True)
    def post(self):
        verify_technician = TechnicianService.verify(request.json)

        if not isinstance(verify_technician, int):
            post_technician = TechnicianService.post(verify_technician)

            if not isinstance(post_technician, int):
                return post_technician

            api.abort(post_technician)

        api.abort(verify_technician)

@api.route("/<id>")
@api.param("id", "The Technician identifier")
class Technician(Resource):
    @api.marshal_with(_technician)
    def get(self, id):
        pass

    @api.expect(_technician, validate=True)
    def patch(self, id):
        patch_technician = TechnicianService.patch(id, request.json)

        if patch_technician == 200:
            return patch_technician

        api.abort(patch_technician)

    @api.expect(_technician, validate=True)
    def delete(self, id):
        delete_technician = TechnicianService.delete(id, request.json)

        if delete_technician == 200:
            return delete_technician

        api.abort(delete_technician)