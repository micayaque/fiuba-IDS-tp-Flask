from flask import Blueprint, jsonify, request, render_template
from db import get_connection

grupos_bp = Blueprint("grupos", __name__)

@grupos_bp.route("/grupos")
def get_grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT grupos.grupo_id, grupos.nombre, materias.nombre AS materia
        FROM grupos
        JOIN materias ON grupos.materia_codigo = materias.materia_codigo
        WHERE NOT grupos.tp_terminado
        """
    )
    grupos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(grupos)