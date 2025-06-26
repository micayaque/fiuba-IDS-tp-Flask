from flask import Blueprint, jsonify
from db import get_connection

grupos_bp = Blueprint("grupos", __name__)

@grupos_bp.route("/cantidad-grupos", methods=["GET"])
def cantidad_grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}
    
    cursor.execute("SELECT MAX(id) AS max_grupo_id FROM grupos")
    res = cursor.fetchone()

    if res['max_grupo_id'] is None:
        data['max_grupo_id'] = 0
    else:
        data['max_grupo_id'] = res['max_grupo_id']

    cursor.close()
    conn.close()

    return jsonify(data)

@grupos_bp.route("/grupos", methods=["GET"])
def grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}
    
    cursor.execute("""
        SELECT grupos.*, materias.nombre AS nombre_materia
        FROM grupos
        JOIN materias ON grupos.codigo_materia = materias.codigo
        WHERE NOT grupos.tp_terminado
    """)
    data['grupos'] = cursor.fetchall()

    for grupo in data['grupos']:
        cursor.execute("SELECT dia, turno FROM horarios_grupos WHERE id_grupo = %s", (grupo['id'],))
        grupo['horarios'] = cursor.fetchall()

        cursor.execute("SELECT u.padron, u.nombre FROM grupos_usuarios g_u JOIN usuarios u ON g_u.padron = u.padron WHERE g_u.id_grupo = %s", (grupo['id'],))
        grupo['integrantes'] = cursor.fetchall()
        grupo['cant_integrantes'] = len(grupo['integrantes'])

    cursor.close()
    conn.close()
    return jsonify(data)


@grupos_bp.route("/grupos", methods=["POST"])
def agregar_grupo():
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")
    integrantes = data.get("integrantes", [])
    creador = data.get("padron_creador")
    horarios = data.get("horarios", [])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if int(maximo_integrantes) < len(integrantes):
        return jsonify({"error": "La cantidad de integrantes ingresados supera la cantidad máxima permitida"}), 400

    cursor.execute("INSERT INTO grupos (codigo_materia, nombre, maximo_integrantes) VALUES (%s, %s, %s)", (materia_codigo, nombre, maximo_integrantes))
    grupo_id = cursor.lastrowid
    cursor.execute("INSERT INTO grupos_usuarios (id_grupo, padron, codigo_materia) VALUES (%s, %s, %s)", (grupo_id, creador, materia_codigo))

    for horario in horarios:
        cursor.execute("INSERT INTO horarios_grupos (id_grupo, dia, turno) VALUES (%s, %s, %s)", (grupo_id, horario["dia"], horario["turno"]))

    integrantes = [padron for padron in integrantes if str(padron) != str(creador)]
    for padron in integrantes:
        cursor.execute("SELECT * FROM grupos_usuarios WHERE padron = %s AND codigo_materia = %s", (padron, materia_codigo))
        invitado = cursor.fetchone()
        if invitado:
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"error": f"El usuario {padron} ya tiene grupo"}), 400


        cursor.execute("SELECT codigo_materia FROM materias_usuarios WHERE padron = %s AND estado = 'cursando'", (padron,))
        materias = cursor.fetchall()
        if materia_codigo not in [m['materia_codigo'] for m in materias]:
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"error": f"El usuario {padron} no está cursando la materia {materia_codigo}"}), 400
 
        
        cursor.execute("INSERT INTO solicitudes_grupos (id_grupo, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'grupo_a_usuario')", (grupo_id, creador, padron))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"grupo_id": grupo_id}), 201


@grupos_bp.route("/grupo/<int:grupo_id>/", methods=["PATCH"])
def editar_grupo(grupo_id):
    data = request.get_json()
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")
    integrantes = data.get("integrantes", [])
    horarios = data.get("horarios", [])
    padron_editor = data.get("padron_editor")    

    if int(maximo_integrantes) < len(integrantes):
        return jsonify({"error": "La cantidad de integrantes ingresados supera la cantidad máxima permitida"}), 400
    

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    integrantes = [padron for padron in integrantes if str(padron).strip()]
    if not integrantes:
        cursor.execute("DELETE FROM grupos WHERE id = %s", (grupo_id,))
        cursor.execute("DELETE FROM grupos_usuarios WHERE id_grupo = %s", (grupo_id,))
        cursor.execute("DELETE FROM horarios_grupos WHERE id_grupo = %s", (grupo_id,))
        cursor.execute("DELETE FROM solicitudes_grupos WHERE id_grupo = %s", (grupo_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Grupo eliminado"}), 200


    cursor.execute("UPDATE grupos SET nombre = %s, maximo_integrantes = %s WHERE id = %s", (nombre, maximo_integrantes, grupo_id))
    cursor.execute("DELETE FROM grupos_usuarios WHERE id_grupo = %s", (grupo_id,))
    cursor.execute("SELECT codigo_materia FROM grupos WHERE id = %s", (grupo_id,))

    materia_codigo = cursor.fetchone()['codigo_materia']
    cursor.execute("INSERT INTO grupos_usuarios (id_grupo, padron, codigo_materia) VALUES (%s, %s, %s)", (grupo_id, padron_editor, materia_codigo))

    integrantes = [padron for padron in integrantes if str(padron) != str(padron_editor)]
    for padron in integrantes:
        cursor.execute("SELECT * FROM grupos_usuarios WHERE padron = %s AND codigo_materia = %s", (padron, materia_codigo))
        invitado = cursor.fetchone()
        if invitado:
            cursor.close()
            conn.close()
            return jsonify({"error": f"El usuario {padron} ya tiene grupo"}), 400


        cursor.execute("SELECT codigo_materia FROM materias_usuarios WHERE padron = %s AND estado = 'cursando'", (padron,))
        materias = cursor.fetchall()
        if materia_codigo not in [m['codigo_materia'] for m in materias]:
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"error": f"El usuario {padron} no está cursando la materia {materia_codigo}"}), 400


        cursor.execute("SELECT * FROM solicitudes_grupos WHERE id_grupo = %s AND padron_receptor = %s", (grupo_id, padron))
        solicitud = cursor.fetchone()
        if not solicitud or solicitud['estado'] == 'rechazada':
            cursor.execute("INSERT INTO solicitudes_grupos (id_grupo, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'grupo_a_usuario')", (grupo_id, padron_editor, padron))
        elif solicitud['estado'] == 'pendiente':
            return jsonify({"error": "Ya enviaste una solicitud antes a uno de los usuarios ingresados"}), 400 
        elif solicitud['estado'] == 'aceptada':
            cursor.execute("INSERT INTO grupos_usuarios (id_grupo, padron, codigo_materia) VALUES (%s, %s, %s)", (grupo_id, padron, materia_codigo))

    cursor.execute("DELETE FROM horarios_grupos WHERE id_grupo = %s", (grupo_id,))
    for horario in horarios:
        cursor.execute("INSERT INTO horarios_grupos (id_grupo, dia, turno) VALUES (%s, %s, %s)", (grupo_id, horario["dia"], horario["turno"]))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Grupo actualizado"}), 200


@grupos_bp.route('/grupo/<int:grupo_id>/estado-tp', methods=['PATCH'])
def cambiar_estado_tp(grupo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT tp_terminado FROM grupos WHERE id = %s", (grupo_id,))
    tp_terminado = cursor.fetchone()
    nuevo_estado = not tp_terminado['tp_terminado']

    cursor.execute("UPDATE grupos SET tp_terminado = %s WHERE id = %s", (nuevo_estado, grupo_id))

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Estado del TP actualizado"}), 200