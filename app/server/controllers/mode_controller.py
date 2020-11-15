from flask import request
from flask_restx import Resource
from ..services.mode_service import ModeService
from ..utils._dtos import ModeDto

api = ModeDto.api
_mode = ModeDto.mode

@api.route("/")
class Mode(Resource):
    @api.marshal_list_with(_mode, envelope="modes")
    def get(self):
        pagination_no = request.args.get("pagination_no", 1, int)

        get_modes = ModeService.get_all(pagination_no)

        if not isinstance(get_modes, int):
            return get_modes

        api.abort(get_modes)

    @api.expect(_mode, validate=True)
    def post(self):
        verify_mode = ModeService.verify(request.json)

        if not isinstance(verify_mode, int):
            post_mode = ModeService.post(verify_mode)

            if not isinstance(post_mode, int):
                return post_mode

            api.abort(post_mode)

        api.abort(verify_mode)

@api.route("/<id>")
@api.param("id", "The Mode identifier")
class Mode(Resource):
    @api.marshal_with(_mode)
    def get(self, id):
        pass

    @api.expect(_mode, validate=True)
    def patch(self, id):
        patch_mode = ModeService.patch(id, request.json)

        if patch_mode == 200:
            return patch_mode

        api.abort(patch_mode)

    @api.expect(_mode, validate=True)
    def delete(self, id):
        delete_mode = ModeService.delete(id, request.json)

        if delete_mode == 200:
            return delete_mode

        api.abort(delete_mode)