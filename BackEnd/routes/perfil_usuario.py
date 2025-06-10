from flask import Blueprint, jsonify, request, render_template
from db import get_connection

perfil_usuario_bp = Blueprint("perfil_usuario", __name__)

@perfil_usuario_bp.route("/usuario/<int:padron>")
def get_perfil_usuario(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT * FROM usuarios WHERE padron = %s
        """, (padron,)
    )
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(resultado)