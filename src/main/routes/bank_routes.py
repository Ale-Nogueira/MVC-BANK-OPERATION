from flask import Blueprint,jsonify

bank_route_bp = Blueprint("bank_routes", __name__)

@bank_route_bp.route("/fisica", methods=["GET"])
def list_pessoa_fisica():
    return jsonify({"Ola": "mundo"}), 200
