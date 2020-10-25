from flask import request
from flask_restx import Resource
from ..services.request_service import RequestService
from ..utils._dtos import RequestDto

api = RequestDto.api
_request = RequestDto.request

@api.route("/")
class Request(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self):
        get_requests_resp = RequestService.get_all()

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

    @api.expect(_request, validate=True)
    def post(self):
        post_request_resp = RequestService.post(request.json)

        if not isinstance(post_request_resp, int):
            return post_request_resp

        api.abort(post_request_resp)

@api.route("/year/<year>")
@api.param("year", "The Year specifier")
class RequestByYear(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, year):
        get_requests_resp = RequestService.get_by_year(year)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/year/<year>/month/<month>")
@api.param("year", "The Request date year")
@api.param("month", "The Request date month")
class RequestByYearAndMonth(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, year, month):
        get_requests_resp = RequestService.get_by_year_and_month(year, month)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/newest")
class NewestRequest(Resource):
    @api.marshal_with(_request)
    def get(self):
        get_request_resp = RequestService.get_newest()

        if not isinstance(get_request_resp, int):
            return get_request_resp

        api.abort(get_request_resp)

@api.route("/oldest")
class OldestRequest(Resource):
    @api.marshal_with(_request)
    def get(self):
        get_request_resp = RequestService.get_oldest()

        if not isinstance(get_request_resp, int):
            return get_request_resp

        api.abort(get_request_resp)

@api.route("/office/<office_id>")
@api.param("office_id", "The Office identifier")
class RequestByOffice(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, office_id):
        get_requests_resp = RequestService.get_by_office(office_id)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/mode/<mode_id>")
@api.param("mode_id", "The Mode identifier")
class RequestByMode(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, mode_id):
        get_requests_resp = RequestService.get_by_mode(mode_id)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/nature/<nature_id>")
@api.param("nature_id", "The Nature identifier")
class RequestByNature(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, nature_id):
        get_requests_resp = RequestService.get_by_nature(nature_id)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/technician/<technician_id>")
@api.param("technician_id", "The Technician identifier")
class RequestByTechnician(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, technician_id):
        get_requests_resp = RequestService.get_by_technician(technician_id)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/result/<result>")
@api.param("result", "The Request result")
class RequestByResult(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, result):
        get_requests_resp = RequestService.get_by_result(result)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/rating/<rating>")
@api.param("rating", "The Request rating")
class RequestByRating(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, rating):
        get_requests_resp = RequestService.get_by_rating(rating)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/detail/<detail>")
@api.param("detail", "The Request detail")
class RequestByDetail(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, detail):
        get_requests_resp = RequestService.get_by_detail(detail)

        if not isinstance(get_requests_resp, int):
            return get_requests_resp

        api.abort(get_requests_resp)

@api.route("/no/<no>/year/<year>")
@api.param("no", "The Request number")
@api.param("year", "The Request detail")
class RequestByNoAndYear(Resource):
    @api.marshal_with(_request)
    def get(self, no, year):
        get_request = RequestService.get_by_no_and_year(no, year)

        if not isinstance(get_request, int):
            return get_request

        api.abort(get_request)

