from flask import Blueprint, jsonify, request
from db import get_connection

grupos_bp = Blueprint("grupos", __name__)


@grupos_bp.route("/grupos", methods=["GET"])
def get_grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}
    
    cursor.execute("""
        SELECT grupos.*, materias.nombre AS nombre_materia
        FROM grupos
        JOIN materias ON grupos.materia_codigo = materias.materia_codigo
        WHERE NOT grupos.tp_terminado
    """)
    data['grupos'] = cursor.fetchall()

    for grupo in data['grupos']:
        cursor.execute("SELECT dia, turno FROM horarios_grupos WHERE grupo_id = %s", (grupo['grupo_id'],))
        grupo['horarios'] = cursor.fetchall()

        cursor.execute("SELECT u.padron, u.nombre FROM grupos_usuarios g_u JOIN usuarios u ON g_u.padron = u.padron WHERE g_u.grupo_id = %s", (grupo['grupo_id'],))
        grupo['integrantes'] = cursor.fetchall()
        grupo['cant_integrantes'] = len(grupo['integrantes'])

    cursor.close()
    conn.close()
    return jsonify(data)


@grupos_bp.route("/materias/<string:materia_codigo>/grupos", methods=["GET"])
def grupos_por_materia(materia_codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}

    cursor.execute("SELECT * FROM materias WHERE materia_codigo = %s", (materia_codigo,))
    materia = cursor.fetchone()
    data['materia'] = materia

    cursor.execute(
        """
        SELECT grupos.*
        FROM grupos
        INNER JOIN materias ON grupos.materia_codigo = materias.materia_codigo
        WHERE grupos.materia_codigo = %s AND NOT grupos.tp_terminado
        """, (materia_codigo,)
    )
    data['grupos'] = cursor.fetchall()

    for grupo in data['grupos']:
        cursor.execute(
            "SELECT dia, turno FROM horarios_grupos WHERE grupo_id = %s",
            (grupo['grupo_id'],)
        )
        grupo['horarios'] = cursor.fetchall()

        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios g_u JOIN usuarios u ON g_u.padron = u.padron WHERE g_u.grupo_id = %s",
            (grupo['grupo_id'],)
        )
        grupo['integrantes'] = cursor.fetchall()
        grupo['cantidad_integrantes'] = len(grupo['integrantes'])

    cursor.close()
    conn.close()

    return jsonify(data), 200


@grupos_bp.route("/materias/<string:materia_codigo>/sin-grupo", methods=["GET"])
def companierxs_sin_grupo(materia_codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}

    cursor.execute("SELECT * FROM materias WHERE materia_codigo = %s", (materia_codigo,))
    data['materia'] = cursor.fetchone()

    cursor.execute("""
    SELECT u.padron, u.nombre, u.carrera
    FROM usuarios u
    JOIN materias_usuarios mu ON u.padron = mu.padron
    WHERE mu.materia_codigo = %s
    AND mu.estado = 'cursando'
    AND u.padron NOT IN (
        SELECT g_u.padron
        FROM grupos_usuarios g_u
        JOIN grupos g ON g_u.grupo_id = g.grupo_id
        WHERE g.materia_codigo = %s
    )
    """, (materia_codigo, materia_codigo))
    data['companierxs'] = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data), 200


@grupos_bp.route("/agregar-grupo", methods=["POST"])
def agregar_grupo():
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")
    integrantes = data.get("integrantes", [])
    creador = data.get("padron_creador")
    horarios = data.get("horarios", [])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO grupos (materia_codigo, nombre, maximo_integrantes) VALUES (%s, %s, %s)", (materia_codigo, nombre, maximo_integrantes))

    grupo_id = cursor.lastrowid

    cursor.execute("INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)", (grupo_id, creador, materia_codigo))

    for horario in horarios:
        cursor.execute("INSERT INTO horarios_grupos (grupo_id, dia, turno) VALUES (%s, %s, %s)", (grupo_id, horario["dia"], horario["turno"]))

    for padron in integrantes:
        if str(padron) != str(creador):
            cursor.execute("INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'grupo_a_usuario')", (grupo_id, creador, padron))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"grupo_id": grupo_id}), 201


@grupos_bp.route("/usuario/<int:grupo_id>/editar-grupo", methods=["POST"])
def editar_grupo(grupo_id):
    data = request.get_json()
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")
    integrantes = data.get("integrantes", [])
    horarios = data.get("horarios", [])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE grupos SET nombre = %s, maximo_integrantes = %s WHERE grupo_id = %s", (nombre, maximo_integrantes, grupo_id))
    cursor.execute("DELETE FROM grupos_usuarios WHERE grupo_id = %s", (grupo_id,))
    cursor.execute("SELECT materia_codigo FROM grupos WHERE grupo_id = %s", (grupo_id,))

    materia_codigo = cursor.fetchone()[0]
    for padron in integrantes:
        if padron:
            cursor.execute("INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)", (grupo_id, padron, materia_codigo))

    cursor.execute("DELETE FROM horarios_grupos WHERE grupo_id = %s", (grupo_id,))

    for horario in horarios:
        cursor.execute(
            "INSERT INTO horarios_grupos (grupo_id, dia, turno) VALUES (%s, %s, %s)", (grupo_id, horario["dia"], horario["turno"]))

    conn.commit()

    cursor.close()
    conn.close()
    return "Grupo actualizado", 200


