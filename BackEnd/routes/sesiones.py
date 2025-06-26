from flask import Blueprint, jsonify, request  
from db import get_connection

sesiones_bp = Blueprint('sesiones', __name__)


@sesiones_bp.route('/sesiones', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    padron = data['padron']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE padron = %s AND contrasena = %s", (padron, password))
    
    usuario = cursor.fetchone()
    if not usuario:
        cursor.close()
        conn.close()
        return jsonify({"error": "Padron o contraseña incorrectos"}), 400

    cursor.close()
    conn.close()
    return jsonify({"message": "Inicio de sesión exitoso"}), 200

