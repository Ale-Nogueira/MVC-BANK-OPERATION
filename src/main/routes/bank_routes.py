from flask import Blueprint,jsonify, request
from src.views.http_types.http_request import HttpRequest
from src.main.composer.bank_composer_pessoa_fisica import list_pessoa_fisica_composer, insert_pessoa_fisica_composer, find_pessoa_fisica_composer
from src.main.composer.bank_composer_pessoa_juridica import list_pessoa_juridica_composer, insert_pessoa_juridica_composer, find_pessoa_juridica_composer
from src.errors.erro_handler import handle_errors

bank_route_bp = Blueprint("bank_routes", __name__)

@bank_route_bp.route("/fisica", methods=["GET"])
def list_pessoa_fisica():
    try:
        http_request = HttpRequest()
        view = list_pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/fisica/insert", methods=["POST"])
def insert_pessoa_fisica():
    try:
        http_request = HttpRequest(body=request.json)
        view = insert_pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/fisica/<person_id>", methods=["GET"])
def find_pessoa_fisica(person_id):
    try:
        http_request = HttpRequest(param={"person_id": person_id})
        view = find_pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/juridica", methods=["GET"])
def list_pessoa_juridica():
    try:
        http_request = HttpRequest()
        view = list_pessoa_juridica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/juridica/insert", methods=["POST"])
def insert_pessoa_juridica():
    try:
        http_request = HttpRequest(body=request.json)
        view = insert_pessoa_juridica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@bank_route_bp.route("/juridica/<person_id>", methods=["GET"])
def find_pessoa_juridica(person_id):
    try:
        http_request = HttpRequest(param={"person_id": person_id})
        view = find_pessoa_juridica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code
