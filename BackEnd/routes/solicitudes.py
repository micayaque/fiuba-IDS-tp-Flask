from flask import Blueprint, jsonify, request
from db import get_connection

solicitudes_bp = Blueprint("solicitudes", __name__)

@solicitudes_bp.route('/solicitudes/<int:padron>', methods=['GET'])
def solicitudes_pendientes(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM solicitudes_grupos WHERE padron_receptor = %s AND estado = 'pendiente'", (padron,))
    solicitudes = cursor.fetchall()

    for solicitud in solicitudes:
        cursor.execute(
            "SELECT dia, turno FROM horarios_grupos WHERE id_grupo = %s",
            (solicitud['id_grupo'],)
        )
        horarios = cursor.fetchall()
        horarios_por_dia_grupo = {}
        for horario in horarios:
            horarios_por_dia_grupo.setdefault(horario["dia"], []).append(horario["turno"])
        solicitud['horarios_grupo'] = horarios_por_dia_grupo

        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios g_u JOIN usuarios u ON g_u.padron = u.padron WHERE g_u.id_grupo = %s",
            (solicitud['id_grupo'],)
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
        return jsonify({"solicitudes_pendientes": solicitudes})
    return jsonify({"solicitudes_pendientes": []}), 200


@solicitudes_bp.route('/solicitudes/<int:solicitud_id>', methods=['PATCH'])
def actualizar_solicitud(solicitud_id):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM solicitudes_grupos WHERE id_solicitud = %s", (solicitud_id,))
    solicitud = cursor.fetchone()

    cursor.execute("SELECT codigo_materia FROM grupos WHERE id = %s", (solicitud['id_grupo'],))
    codigo_materia = cursor.fetchone()['codigo_materia']

    tipo = solicitud['tipo']
    if nuevo_estado == 'aceptada':
        if tipo == 'usuario_a_grupo':
            cursor.execute("INSERT INTO grupos_usuarios (id_grupo, padron, codigo_materia) VALUES (%s, %s, %s)", (solicitud['id_grupo'], solicitud['padron_emisor'], codigo_materia))
            cursor.execute("UPDATE solicitudes_grupos SET estado = 'aceptada' WHERE id_grupo = %s AND padron_emisor = %s", (solicitud['id_grupo'], solicitud['padron_emisor']))
        else:
            cursor.execute("INSERT INTO grupos_usuarios (id_grupo, padron, codigo_materia) VALUES (%s, %s, %s)", (solicitud['id_grupo'], solicitud['padron_receptor'], codigo_materia))
            cursor.execute("UPDATE solicitudes_grupos SET estado = 'aceptada' WHERE id_grupo = %s AND padron_receptor = %s", (solicitud['id_grupo'], solicitud['padron_receptor']))
    else:
        if tipo == 'usuario_a_grupo':
            cursor.execute("UPDATE solicitudes_grupos SET estado = 'rechazada' WHERE id_grupo = %s AND padron_emisor = %s", (solicitud['id_grupo'], solicitud['padron_emisor']))
        else:
            cursor.execute("UPDATE solicitudes_grupos SET estado = 'rechazada' WHERE id_grupo = %s AND padron_receptor = %s", (solicitud['id_grupo'], solicitud['padron_receptor']))

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Solicitud actualizada"}), 200


@solicitudes_bp.route('/solicitudes/grupos/<int:grupo_id>', methods=['POST'])
def solicitar_unirse_grupo(grupo_id):
    data = request.get_json()
    padron_emisor = data.get('padron_emisor')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as cantidad_integrantes FROM grupos_usuarios WHERE id_grupo = %s", (grupo_id,))
    cantidad_integrantes = cursor.fetchone()['cantidad_integrantes']
    cursor.execute("SELECT maximo_integrantes FROM grupos WHERE id = %s", (grupo_id,))
    maximo = cursor.fetchone()['maximo_integrantes']
    if cantidad_integrantes == maximo:
        cursor.close()
        conn.close()
        return jsonify({"error": "El grupo ya está lleno"}), 400


    cursor.execute("SELECT codigo_materia FROM grupos WHERE id = %s", (grupo_id,))
    grupo_materia = cursor.fetchone()

    cursor.execute("SELECT * FROM grupos_usuarios WHERE padron = %s AND codigo_materia = %s", (padron_emisor, grupo_materia['codigo_materia']))
    grupo_usuario = cursor.fetchone()
    if grupo_usuario:
        cursor.close()
        conn.close()
        return jsonify({"error": "Ya estás en un grupo. Salí del grupo primero para poder enviar solicitud a otro."}), 400

    cursor.execute("SELECT * FROM materias_usuarios WHERE padron = %s AND estado = 'cursando'", (padron_emisor,))
    materias = cursor.fetchall()
    if grupo_materia['codigo_materia'] not in [m['codigo_materia'] for m in materias]:
        cursor.close()
        conn.close()
        return jsonify({"error": "No estás cursando la materia " + grupo_materia['codigo_materia']}), 400

    cursor.execute("SELECT * FROM solicitudes_grupos WHERE id_grupo = %s AND padron_emisor = %s AND estado = 'pendiente'", (grupo_id, padron_emisor))
    solicitud_pendiente = cursor.fetchone()
    if solicitud_pendiente:
        cursor.close()
        conn.close()
        return jsonify({"error": "Ya existe una solicitud pendiente para este grupo"}), 400

    cursor.execute("SELECT padron FROM grupos_usuarios WHERE id_grupo = %s",(grupo_id,))
    integrantes = cursor.fetchall()

    for integrante in integrantes:
        padron_receptor = integrante['padron']
        cursor.execute(
            "INSERT INTO solicitudes_grupos (id_grupo, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'usuario_a_grupo')", (grupo_id, padron_emisor, padron_receptor))

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Solicitud enviada"}), 201


@solicitudes_bp.route('/solicitudes/usuarios/<int:padron_receptor>', methods=['POST'])
def enviar_solicitud_companierx(padron_receptor):
    data = request.get_json()
    padron_emisor = data.get('padron_emisor')
    materia_codigo = data.get('materia_codigo')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_grupo FROM grupos_usuarios WHERE padron = %s AND codigo_materia = %s", (padron_emisor, materia_codigo))
    grupo = cursor.fetchone()
    if grupo:
        cursor.execute("SELECT COUNT(*) as cantidad_integrantes FROM grupos_usuarios WHERE id_grupo = %s", (grupo['id_grupo'],))
        cantidad_integrantes = cursor.fetchone()['cantidad_integrantes']
        cursor.execute("SELECT maximo_integrantes FROM grupos WHERE id = %s", (grupo['id_grupo'],))
        maximo = cursor.fetchone()['maximo_integrantes']
        if cantidad_integrantes == maximo:
            cursor.close()
            conn.close()
            return jsonify({"error": "El grupo ya está lleno"}), 400
    

    cursor.execute("SELECT * FROM materias_usuarios WHERE padron = %s AND estado = 'cursando'", (padron_emisor,))
    materias = cursor.fetchall()
    if materia_codigo not in [m['codigo_materia'] for m in materias]:
        cursor.close()
        conn.close()
        return jsonify({"error": "No estás cursando la materia " + materia_codigo}), 400

    cursor.execute("SELECT * FROM solicitudes_grupos WHERE padron_emisor = %s AND padron_receptor = %s AND estado = 'pendiente'", (padron_emisor, padron_receptor))
    solicitud_pendiente = cursor.fetchone()
    if solicitud_pendiente:
        cursor.close()
        conn.close()
        return jsonify({"error": "Ya enviaste una solicitud a este usuario"}), 400


    if grupo is not None:
        grupo_id = grupo['id_grupo']
        cursor.execute("INSERT INTO solicitudes_grupos (id_grupo, padron_emisor, padron_receptor, estado, tipo) VALUES (%s, %s, %s, 'pendiente', 'grupo_a_usuario')", (grupo_id, padron_emisor, padron_receptor))
    else:
        cursor.execute("INSERT INTO grupos (codigo_materia) VALUES (%s)", (materia_codigo,))
        grupo_id = cursor.lastrowid
        cursor.execute("INSERT INTO grupos_usuarios (id_grupo, padron, codigo_materia) VALUES (%s, %s, %s)", (grupo_id, padron_emisor, materia_codigo))
        cursor.execute("UPDATE grupos SET nombre = %s WHERE id = %s", (f"Grupo {grupo_id}", grupo_id))
        cursor.execute("INSERT INTO solicitudes_grupos (id_grupo, padron_emisor, padron_receptor, estado, tipo) VALUES (%s, %s, %s, 'pendiente', 'usuario_a_usuario')", (grupo_id, padron_emisor, padron_receptor))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Solicitud enviada"}), 201