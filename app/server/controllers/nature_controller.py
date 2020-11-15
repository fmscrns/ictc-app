from flask import request
from flask_restx import Resource
from ..services.nature_service import NatureService
from ..utils._dtos import NatureDto

api = NatureDto.api
_nature = NatureDto.nature

@api.route("/")
class NatureList(Resource):
    @api.marshal_list_with(_nature, envelope="natures")
    def get(self):
        pagination_no = request.args.get("pagination_no", 1, int)
        order_command = request.args.get("order_command", "NAME_ASC", str)

        get_natures = NatureService.get_all(pagination_no, order_command)

        if not isinstance(get_natures, int):
            return get_natures

        api.abort(get_natures)

    @api.expect(_nature, validate=True)
    def post(self):
        verify_nature = NatureService.verify(request.json)

        if not isinstance(verify_nature, int):
            post_nature = NatureService.post(request.json)

            if not isinstance(post_nature, int):
                return post_nature

            api.abort(post_nature)

        api.abort(verify_nature)

@api.route("/office/<office_id>")
@api.param("office_id", "The Office identifier")
class NatureListByOffice(Resource):
    @api.marshal_list_with(_nature, envelope="natures")
    def get(self, office_id):
        pagination_no = request.args.get("pagination_no", 1, int)
        order_command = request.args.get("order_command", "NAME_ASC", str)

        get_natures = NatureService.get_by_office(office_id, pagination_no, order_command)

        if not isinstance(get_natures, int):
            return get_natures

        api.abort(get_natures)

@api.route("/<id>")
@api.param("id", "The Nature identifier")
class Nature(Resource):
    @api.marshal_with(_nature)
    def get(self, id):
        pass

    @api.expect(_nature, validate=True)
    def patch(self, id):
        patch_nature = NatureService.patch(id, request.json)

        if patch_nature == 200:
            return patch_nature

        api.abort(patch_nature)

    @api.expect(_nature, validate=True)
    def delete(self, id):
        delete_nature = NatureService.delete(id, request.json)

        if delete_nature == 200:
            return delete_nature

        api.abort(delete_nature)