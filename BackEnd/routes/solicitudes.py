from flask import Blueprint, jsonify, request, render_template
from db import get_connection

solicitudes_bp = Blueprint("solicitudes", __name__)

@solicitudes_bp.route('/solicitud/<int:solicitud_id>', methods=['GET'])
def get_solicitud(solicitud_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT s_g.*, g.materia_codigo
        FROM solicitudes_grupos s_g
        JOIN grupos g ON s_g.grupo_id = g.grupo_id
        WHERE s_g.solicitud_id = %s
        """,
        (solicitud_id,)
    )
    solicitud = cursor.fetchone()

    cursor.close()
    conn.close()
    if solicitud:
        return jsonify(solicitud)
    else:
        return "Solicitud no encontrada", 404
    


@solicitudes_bp.route('/solicitudes/<int:solicitud_id>/actualizar', methods=['POST'])
def actualizar_solicitud(solicitud_id):
    data = request.get_json()
    nuevo_estado = data.get('estado')  # 'aceptada' o 'rechazada'

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT grupo_id, padron_emisor, tipo FROM solicitudes_grupos WHERE solicitud_id = %s",
        (solicitud_id,)
    )
    solicitud = cursor.fetchone()

    grupo_id = solicitud['grupo_id']
    padron_emisor = solicitud['padron_emisor']
    tipo = solicitud['tipo']

    cursor.execute(
        """
        UPDATE solicitudes_grupos
        SET estado = %s
        WHERE grupo_id = %s AND padron_emisor = %s AND tipo = %s AND estado = 'pendiente'
        """,
        (nuevo_estado, grupo_id, padron_emisor, tipo)
    )

    conn.commit()

    cursor.close()
    conn.close()
    return '', 200