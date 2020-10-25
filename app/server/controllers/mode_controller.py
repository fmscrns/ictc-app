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
        get_modes = ModeService.get_all()

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