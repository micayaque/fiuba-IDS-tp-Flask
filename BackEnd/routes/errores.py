from flask import Blueprint, jsonify, request
from db import get_connection

error_bp = Blueprint("errores", __name__)

@error_bp.errorhandler(404)
def error(e):
    return jsonify({"error": "Recurso no encontrado"}), 404