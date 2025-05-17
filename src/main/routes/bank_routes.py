from flask import Blueprint,jsonify, request
from src.views.http_types.http_request import HttpRequest
from src.main.composer.bank_composer_pessoa_fisica import list_pessoa_fisica_composer, insert_pessoa_fisica_composer, find_pessoa_fisica_composer

bank_route_bp = Blueprint("bank_routes", __name__)

@bank_route_bp.route("/fisica", methods=["GET"])
def list_pessoa_fisica():
    http_request = HttpRequest()
    view = list_pessoa_fisica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/fisica/insert", methods=["POST"])
def insert_pessoa_fisica():
    http_request = HttpRequest(body=request.json)
    view = insert_pessoa_fisica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/fisica/<person_id>", methods=["GET"])
def find_pessoa_fisica(person_id):
    http_request = HttpRequest(param={"person_id": person_id})
    view = find_pessoa_fisica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code
