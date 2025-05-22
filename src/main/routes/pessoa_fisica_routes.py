from flask import Blueprint,jsonify, request
from src.views.http_types.http_request import HttpRequest
from src.main.composer.pessoa_fisica_composer import saque_pessoa_fisica_composer, extrato_pessoa_fisica_composer
from src.errors.erro_handler import handle_errors


pessoa_fisica_route_bp = Blueprint ("pessoa_fisica_routes", __name__)

@pessoa_fisica_route_bp.route("/fisica/saque", methods=["PUT"])
def saque_pessoa_fisica():
    try:
        http_request = HttpRequest(body=request.json)
        view = saque_pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@pessoa_fisica_route_bp.route("/fisica/extrato", methods=["GET"])
def extrato_pessoa_fisica():
    try:
        http_request = HttpRequest(body=request.json)
        view = extrato_pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code
