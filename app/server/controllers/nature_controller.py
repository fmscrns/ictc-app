from flask import request
from flask_restx import Resource
from ..services.nature_service import NatureService
from ..utils._dtos import NatureDto

api = NatureDto.api
_nature = NatureDto.nature

@api.route("/")
class Nature(Resource):
    @api.marshal_list_with(_nature, envelope="natures")
    def get(self):
        get_natures = NatureService.get_all()

        if not isinstance(get_natures, int):
            return get_natures

        api.abort(get_natures)

    @api.expect(_nature, validate=True)
    def post(self):
        verify_nature = NatureService.verify(request.json)

        if not isinstance(verify_nature, int):
            post_nature = NatureService.post(verify_nature)

            if not isinstance(post_nature, int):
                return post_nature

            api.abort(post_nature)

        api.abort(verify_nature)