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
    nuevo_estado = data.get('estado')
    materia_codigo = data.get('materia_codigo')
    padron_emisor = data.get('padron_emisor')
    padron_receptor = data.get('padron_receptor')
    grupo_id = data.get('grupo_id')
    tipo = data.get('tipo')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        UPDATE solicitudes_grupos
        SET estado = %s
        WHERE grupo_id = %s AND padron_receptor = %s AND tipo = %s AND estado = 'pendiente'
        """,
        (nuevo_estado, grupo_id, padron_receptor, tipo)
    )

    if tipo == 'usuario_a_grupo':
        if nuevo_estado == 'aceptada':
            cursor.execute(
                """
                INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo)
                VALUES (%s, %s, %s)
                """,
                (grupo_id, padron_emisor, materia_codigo)
            )
    elif tipo == 'grupo_a_usuario' or tipo == 'usuario_a_usuario':
        if nuevo_estado == 'aceptada':
            cursor.execute(
                """
                INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo)
                VALUES (%s, %s, %s)
                """,
                (grupo_id, padron_receptor, materia_codigo)
            )

    conn.commit()

    cursor.close()
    conn.close()
    return '', 200




@solicitudes_bp.route('/solicitud/grupo-a-usuario', methods=['POST'])
def crear_solicitud_grupo_a_usuario():
    data = request.get_json()
    grupo_id = data['grupo_id']
    padron_emisor = data['padron_emisor']
    padron_receptor = data['padron_receptor']
    # materia_codigo = data['materia_codigo']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, tipo, estado)
        VALUES (%s, %s, %s, 'grupo_a_usuario', 'pendiente')
    """, (grupo_id, padron_emisor, padron_receptor))

    conn.commit()

    cursor.close()
    conn.close()
    return '', 201




@solicitudes_bp.route('/solicitud/usuario-a-usuario', methods=['POST'])
def crear_solicitud_usuario_a_usuario():
    data = request.get_json()
    padron_emisor = data['padron_emisor']
    padron_receptor = data['padron_receptor']
    materia_codigo = data['materia_codigo']
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO grupos (materia_codigo) VALUES (%s)",
        (materia_codigo,)
    )
    grupo_id = cursor.lastrowid

    cursor.execute(
        "UPDATE grupos SET nombre = %s WHERE grupo_id = %s",
        (f"Grupo {grupo_id}", grupo_id)
    )        

    cursor.execute(
        "INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)",
        (grupo_id, padron_emisor, materia_codigo)
    )

    cursor.execute("""
        INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, tipo, estado)
        VALUES (%s, %s, %s, 'usuario_a_usuario', 'pendiente')
    """, (grupo_id, padron_emisor, padron_receptor))

    conn.commit()

    cursor.close()
    conn.close()
    return '', 201