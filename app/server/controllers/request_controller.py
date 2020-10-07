import os
from datetime import datetime
from flask import render_template
from flask_restx import Resource
from sqlalchemy import extract
from ..services.request_service import RequestService
from ..utils.dtos import RequestDto

api = RequestDto.api
_request = RequestDto.request

@api.route("/")
class Request(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self):
        get_requests = RequestService.get_all()

        if not isinstance(get_requests, int):
            return get_requests

        api.abort(get_requests)

    def post(self):
        return "hello"

@api.route("/year/<year>")
@api.param("year", "The Year specifier")
class RequestByYear(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, year):
        get_requests = RequestService.get_by_year(year)

        if not isinstance(get_requests, int):
            return get_requests

        api.abort(get_requests)

@api.route("/year/<year>/month/<month>")
@api.param("year", "The Year specifier")
@api.param("month", "The Month specifier")
class RequestByYearAndMonth(Resource):
    @api.marshal_list_with(_request, envelope="requests")
    def get(self, year, month):
        get_requests = RequestService.get_by_year_and_month(year, month)

        if not isinstance(get_requests, int):
            return get_requests

        api.abort(get_requests)

@api.route("/newest")
class NewestRequest(Resource):
    @api.marshal_with(_request)
    def get(self):
        get_request = RequestService.get_newest()

        if not isinstance(get_request, int):
            return get_request

        api.abort(get_request)

@api.route("/oldest")
class OldestRequest(Resource):
    @api.marshal_with(_request)
    def get(self):
        get_request = RequestService.get_oldest()

        if not isinstance(get_request, int):
            return get_request

        api.abort(get_request)