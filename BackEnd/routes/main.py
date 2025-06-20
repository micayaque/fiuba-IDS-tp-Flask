from flask import Blueprint, jsonify
from db import get_connection

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}
    
    cursor.execute( " SELECT COUNT(grupo_id) AS cant_grupos FROM grupos " )
    res = cursor.fetchone()

    if res['cant_grupos'] is None:
        data['cant_grupos'] = 0
    else:
        data['cant_grupos'] = res['cant_grupos']

    cursor.close()
    conn.close()

    return jsonify(data)