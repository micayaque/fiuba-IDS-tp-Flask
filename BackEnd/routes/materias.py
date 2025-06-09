from flask import Blueprint, jsonify, request
from db import get_connection

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/materias")
def get_materias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT DISTINCT materias.materia_codigo, materias.nombre 
        FROM materias
        INNER JOIN grupos ON materias.materia_codigo = grupos.materia_codigo
        """)
    materias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(materias)