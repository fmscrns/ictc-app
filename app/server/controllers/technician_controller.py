from flask import request
from flask_restx import Resource
from ..services.technician_service import TechnicianService
from ..utils._dtos import TechnicianDto

api = TechnicianDto.api
_technician = TechnicianDto.technician

@api.route("/")
class Technician(Resource):
    @api.marshal_list_with(_technician, envelope="technicians")
    def get(self):
        get_technicians = TechnicianService.get_all()

        if not isinstance(get_technicians, int):
            return get_technicians

        api.abort(get_technicians)