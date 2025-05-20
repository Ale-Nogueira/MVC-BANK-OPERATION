from flask import Blueprint,jsonify, request
from src.views.http_types.http_request import HttpRequest
from src.main.composer.pessoa_juridica_composer import saque_pessoa_juridica_composer, extrato_pessoa_juridica_composer

pessoa_juridica_route_bp = Blueprint ("pessoa_juridica_routes", __name__)

@pessoa_juridica_route_bp.route("/juridica/saque", methods=["PUT"])
def saque_pessoa_juridica():
    http_request = HttpRequest(body=request.json)
    view = saque_pessoa_juridica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code

@pessoa_juridica_route_bp.route("/juridica/extrato", methods=["GET"])
def extrato_pessoa_juridica():
    http_request = HttpRequest(body=request.json)
    view = extrato_pessoa_juridica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code
