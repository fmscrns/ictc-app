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
        pagination_no = request.args.get("pagination_no", 1, int)
        order_command = request.args.get("order_command", None, str)

        get_offices = OfficeService.get_all(pagination_no) if order_command == None else OfficeService.get_all_w_totreq(pagination_no, order_command)

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

@api.route("/<id>")
@api.param("id", "The Office identifier")
class Office(Resource):
    @api.marshal_list_with(_office)
    def get(self, id):
        pass

    @api.expect(_office, validate=True)
    def patch(self, id):
        patch_office = OfficeService.patch(id, request.json)

        if patch_office == 200:
            return patch_office

        api.abort(patch_office)

    @api.expect(_office, validate=True)
    def delete(self, id):
        delete_office = OfficeService.delete(id, request.json)

        if delete_office == 200:
            return delete_office

        api.abort(delete_office)