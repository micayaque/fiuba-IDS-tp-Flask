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
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(usuario)

@perfil_usuario_bp.route("/usuario/<int:padron>/editar", methods=["POST"])
def editar_perfil_usuario(padron):
    data = request.get_json()
    campo = data.get("campo")
    valor = data.get("valor")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE usuarios SET {campo} = %s WHERE padron = %s", (valor, padron))
    conn.commit()

    cursor.close()
    conn.close()
    return "Perfil actualizado", 200