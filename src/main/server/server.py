from flask import Flask
from flask_cors import CORS
from src.models.sqlite.setting.connection import db_connection_handler
from src.main.routes.bank_routes import bank_route_bp

db_connection_handler.connect_to_db()

app = Flask(__name__)
CORS(app)

app.register_blueprint(bank_route_bp)
