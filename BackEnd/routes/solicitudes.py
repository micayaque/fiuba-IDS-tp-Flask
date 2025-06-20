from flask import Blueprint, jsonify, request
from db import get_connection

solicitudes_bp = Blueprint("solicitudes", __name__)

@solicitudes_bp.route('/usuario/<int:padron>/solicitudes-pendientes', methods=['GET'])
def solicitudes_pendientes(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s_g.*, g.nombre AS grupo_nombre, g.materia_codigo, m.nombre AS materia_nombre,
               u.nombre AS nombre_emisor
        FROM solicitudes_grupos s_g
        JOIN grupos g ON s_g.grupo_id = g.grupo_id
        JOIN materias m ON g.materia_codigo = m.materia_codigo
        JOIN usuarios u ON s_g.padron_emisor = u.padron
        WHERE s_g.padron_receptor = %s AND s_g.estado = 'pendiente'
    """, (padron,))
    solicitudes = cursor.fetchall()

    for solicitud in solicitudes:
        cursor.execute(
            "SELECT dia, turno FROM horarios_grupos WHERE grupo_id = %s",
            (solicitud['grupo_id'],)
        )
        horarios = cursor.fetchall()
        horarios_por_dia_grupo = {}
        for horario in horarios:
            horarios_por_dia_grupo.setdefault(horario["dia"], []).append(horario["turno"])
        solicitud['horarios_grupo'] = horarios_por_dia_grupo

        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios g_u JOIN usuarios u ON g_u.padron = u.padron WHERE g_u.grupo_id = %s",
            (solicitud['grupo_id'],)
        )
        solicitud['integrantes'] = cursor.fetchall()

        cursor.execute(
            "SELECT dia, turno FROM horarios_usuarios WHERE padron = %s",
            (solicitud['padron_emisor'],)
        )
        horarios_emisor = cursor.fetchall()
        horarios_por_dia_emisor = {}
        for horario in horarios_emisor:
            horarios_por_dia_emisor.setdefault(horario["dia"], []).append(horario["turno"])
        solicitud['horarios_emisor'] = horarios_por_dia_emisor

    cursor.close()
    conn.close()    
    if solicitudes:
        return jsonify({"pendientes": solicitudes})
    return jsonify({"pendientes": []}), 200


@solicitudes_bp.route('/solicitudes/<int:solicitud_id>/actualizar', methods=['POST'])
def actualizar_solicitud(solicitud_id):
    data = request.get_json()
    nuevo_estado = data.get('estado')

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

    if solicitud['tipo'] == 'usuario_a_grupo':
        if nuevo_estado == 'aceptada':
            cursor.execute(
                """
                INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo)
                VALUES (%s, %s, %s)
                """,
                (solicitud['grupo_id'], solicitud['padron_emisor'], solicitud['materia_codigo'])
            )
        cursor.execute(" UPDATE solicitudes_grupos SET estado = %s WHERE grupo_id = %s AND padron_emisor = %s", (nuevo_estado, solicitud['grupo_id'], solicitud['padron_emisor']))

    elif solicitud['tipo'] == 'grupo_a_usuario' or solicitud['tipo'] == 'usuario_a_usuario':
        if nuevo_estado == 'aceptada':
            cursor.execute(
                """
                INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo)
                VALUES (%s, %s, %s)
                """,
                (solicitud['grupo_id'], solicitud['padron_receptor'], solicitud['materia_codigo'])
            )
        cursor.execute("UPDATE solicitudes_grupos SET estado = %s WHERE solicitud_id = %s", (nuevo_estado, solicitud_id))

    conn.commit()

    cursor.close()
    conn.close()
    return '', 200


@solicitudes_bp.route('/grupos/<int:grupo_id>/solicitar-unirse-grupo', methods=['POST'])
def solicitar_unirse_grupo(grupo_id):
    data = request.get_json()
    padron_emisor = data.get('padron_emisor')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT padron FROM grupos_usuarios WHERE grupo_id = %s",(grupo_id,))
    integrantes = cursor.fetchall()

    for integrante in integrantes:
        padron_receptor = integrante['padron']
        cursor.execute(
            "INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'usuario_a_grupo')", (grupo_id, padron_emisor, padron_receptor))

    conn.commit()

    cursor.close()
    conn.close()
    return '', 201


@solicitudes_bp.route('/enviar-solicitud-companierx/<string:materia_codigo>/<int:padron_emisor>/<int:padron_receptor>', methods=['POST'])
def enviar_solicitud_companierx(materia_codigo, padron_emisor, padron_receptor):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT grupo_id FROM grupos_usuarios WHERE padron = %s AND materia_codigo = %s", (padron_emisor, materia_codigo))
    row = cursor.fetchone()
    if row is not None:
        grupo_id = row['grupo_id']
        cursor.execute("INSERT INTO solicitudes_companierxs (grupo_id, padron_emisor, padron_receptor, estado, tipo) VALUES (%s, %s, %s, 'pendiente', 'grupo_a_usuario')", (grupo_id, padron_emisor, padron_receptor))
    else:
        cursor.execute("INSERT INTO grupos (materia_codigo) VALUES (%s)", (materia_codigo,))
        grupo_id = cursor.lastrowid
        cursor.execute("INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)", (grupo_id, padron_emisor, materia_codigo))
        cursor.execute("UPDATE grupos SET nombre = %s WHERE grupo_id = %s", (f"Grupo {grupo_id}", grupo_id))
        cursor.execute("INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, estado, tipo) VALUES (%s, %s, %s, 'pendiente', 'usuario_a_usuario')", (grupo_id, padron_emisor, padron_receptor))

    conn.commit()

    cursor.close()
    conn.close()
    return '', 201















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