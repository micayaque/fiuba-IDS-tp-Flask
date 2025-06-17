from flask import Blueprint, jsonify, request
from db import get_connection

grupos_bp = Blueprint("grupos", __name__)

@grupos_bp.route("/grupos", methods=["GET"])
def get_grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        """
        SELECT grupos.*, materias.nombre AS nombre_materia
        FROM grupos
        JOIN materias ON grupos.materia_codigo = materias.materia_codigo
        WHERE NOT grupos.tp_terminado
        """
    )    
    grupos = cursor.fetchall()

    for grupo in grupos:
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
    return jsonify(grupos)


@grupos_bp.route("/agregar-grupo", methods=["POST"])
def crear_grupo():
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")
    integrantes = data.get("integrantes", [])
    creador = data.get("padron_creador")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO grupos (materia_codigo, nombre, maximo_integrantes) VALUES (%s, %s, %s)",
        (materia_codigo, nombre, maximo_integrantes)
    )

    grupo_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)",
        (grupo_id, creador, materia_codigo)
    )

    for padron in integrantes:
        if str(padron) != str(creador):
            cursor.execute(
                "INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'grupo_a_usuario')",
                (grupo_id, creador, padron)
            )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"grupo_id": grupo_id}), 201


@grupos_bp.route("/grupos/<int:grupo_id>/agregar-integrante", methods=["POST"])
def agregar_integrante_a_grupo(grupo_id):
    data = request.get_json()
    padron = data.get("padron")
    materia_codigo = data.get("materia_codigo")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)",
        (grupo_id, padron, materia_codigo)
    )
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return "Integrante agregado", 201


@grupos_bp.route("/grupos/<int:grupo_id>/agregar-horarios-grupo", methods=["POST"])
def agregar_horarios_grupo(grupo_id):
    data = request.get_json()
    horarios = data.get("horarios", [])

    conn = get_connection()
    cursor = conn.cursor()

    for horario in horarios:
        cursor.execute(
            "INSERT INTO horarios_grupos (grupo_id, dia, turno) VALUES (%s, %s, %s)",
            (grupo_id, horario["dia"], horario["turno"])
        )

    conn.commit()

    cursor.close()
    conn.close()
    return "Horarios agregados", 201


@grupos_bp.route('/grupos/<int:grupo_id>/solicitar-unirse-grupo', methods=['POST'])
def solicitar_unirse_grupo(grupo_id):
    data = request.get_json()
    padron_emisor = data.get('padron_emisor')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT padron FROM grupos_usuarios WHERE grupo_id = %s",
        (grupo_id,)
    )
    integrantes = cursor.fetchall()

    for integrante in integrantes:
        padron_receptor = integrante['padron']
        cursor.execute(
            "INSERT INTO solicitudes_grupos (grupo_id, padron_emisor, padron_receptor, tipo) VALUES (%s, %s, %s, 'usuario_a_grupo')",
            (grupo_id, padron_emisor, padron_receptor)
        )

    conn.commit()

    cursor.close()
    conn.close()
    return '', 201



@grupos_bp.route("/grupos/<int:grupo_id>/editar", methods=["POST"])
def editar_grupo(grupo_id):
    data = request.get_json()
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")
    integrantes = data.get("integrantes", [])
    horarios = data.get("horarios", [])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE grupos SET nombre = %s, maximo_integrantes = %s WHERE grupo_id = %s",
        (nombre, maximo_integrantes, grupo_id)
    )

    cursor.execute("DELETE FROM grupos_usuarios WHERE grupo_id = %s", (grupo_id,))
    cursor.execute("SELECT materia_codigo FROM grupos WHERE grupo_id = %s", (grupo_id,))
    materia_codigo = cursor.fetchone()[0]
    for padron in integrantes:
        if padron:
            cursor.execute(
                "INSERT INTO grupos_usuarios (grupo_id, padron, materia_codigo) VALUES (%s, %s, %s)",
                (grupo_id, padron, materia_codigo)
            )

    cursor.execute("DELETE FROM horarios_grupos WHERE grupo_id = %s", (grupo_id,))
    for horario in horarios:
        cursor.execute(
            "INSERT INTO horarios_grupos (grupo_id, dia, turno) VALUES (%s, %s, %s)",
            (grupo_id, horario["dia"], horario["turno"])
        )

    conn.commit()
    cursor.close()
    conn.close()
    return "Grupo actualizado", 200