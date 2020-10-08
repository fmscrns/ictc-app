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