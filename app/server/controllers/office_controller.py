from flask import request
from flask_restx import Resource
from ..services.office_service import OfficeService
from ..utils._dtos import OfficeDto

api = OfficeDto.api
_office = OfficeDto.office

@api.route("/")
class Office(Resource):
    @api.marshal_list_with(_office, envelope="offices")
    def get(self):
        get_offices = OfficeService.get_all()

        if not isinstance(get_offices, int):
            return get_offices

        api.abort(get_offices)