from flask import request
from flask_restx import Resource
from ..services.office_service import OfficeService
from ..utils._dtos import OfficeDto

api = OfficeDto.api
_office = OfficeDto.office

@api.route("/")
class OfficeList(Resource):
    @api.marshal_list_with(_office, envelope="offices")
    def get(self):
        get_offices = OfficeService.get_all()

        if not isinstance(get_offices, int):
            return get_offices

        api.abort(get_offices)

    @api.expect(_office, validate=True)
    def post(self):
        verify_office = OfficeService.verify(request.json)

        if not isinstance(verify_office, int):
            post_office = OfficeService.post(verify_office)

            if not isinstance(post_office, int):
                return post_office

            api.abort(post_office)

        api.abort(verify_office)

    @api.expect(_office, validate=True)
    def patch(self):
        patch_office = OfficeService.patch(request.json)

        if patch_office == 200:
            return patch_office

        api.abort(patch_office)

    @api.expect(_office, validate=True)
    def delete(self):
        delete_office = OfficeService.delete(request.json)

        if delete_office == 200:
            return delete_office

        api.abort(delete_office)