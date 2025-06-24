from flask import Blueprint, jsonify
from db import get_connection

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}
    
    cursor.execute("SELECT MAX(grupo_id) AS max_grupo_id FROM grupos")
    res = cursor.fetchone()

    if res['max_grupo_id'] is None:
        data['max_grupo_id'] = 0
    else:
        data['max_grupo_id'] = res['max_grupo_id']

    cursor.close()
    conn.close()

    return jsonify(data)