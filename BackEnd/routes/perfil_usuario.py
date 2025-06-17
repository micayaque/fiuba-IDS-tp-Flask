from flask import Blueprint, jsonify, request, render_template
from db import get_connection

perfil_usuario_bp = Blueprint("perfil_usuario", __name__)

# Datos del usuario
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

@perfil_usuario_bp.route("/usuario/<int:padron>/editar-perfil", methods=["POST"])
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


# Materias cursando
@perfil_usuario_bp.route("/usuario/<int:padron>/materias-cursando", methods=["GET"])
def materias_cursando(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m_u.materia_codigo, m.nombre
        FROM materias_usuarios m_u
        JOIN materias m ON m_u.materia_codigo = m.materia_codigo
        WHERE m_u.padron = %s AND m_u.estado = 'cursando'
        """, (padron,)
    )

    materias = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(materias), 200

@perfil_usuario_bp.route("/usuario/<int:padron>/agregar-materia-cursando", methods=["POST"])
def agregar_materia_cursando(padron):
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO materias_usuarios (padron, materia_codigo, estado) VALUES (%s, %s, 'cursando')",
        (padron, materia_codigo)
    )
    conn.commit()

    cursor.close()
    conn.close()
    return "Materia agregada", 201

@perfil_usuario_bp.route("/usuario/<int:padron>/eliminar-materia-cursando", methods=["POST"])
def eliminar_materia_cursando(padron):
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM materias_usuarios WHERE padron = %s AND materia_codigo = %s AND estado = 'cursando'",
        (padron, materia_codigo)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return "Materia eliminada", 200


# Materias aprobadas
@perfil_usuario_bp.route("/usuario/<int:padron>/materias-aprobadas", methods=["GET"])
def materias_aprobadas(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m_u.materia_codigo, m.nombre
        FROM materias_usuarios m_u
        JOIN materias m ON m_u.materia_codigo = m.materia_codigo
        WHERE m_u.padron = %s AND m_u.estado = 'aprobada'
        """, (padron,)
    )

    materias = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(materias), 200


@perfil_usuario_bp.route("/usuario/<int:padron>/agregar-materia-aprobada", methods=["POST"])
def agregar_materia_aprobada(padron):
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO materias_usuarios (padron, materia_codigo, estado) VALUES (%s, %s, 'aprobada')",
        (padron, materia_codigo)
    )
    conn.commit()

    cursor.close()
    conn.close()
    return "Materia agregada", 201

@perfil_usuario_bp.route("/usuario/<int:padron>/eliminar-materia-aprobada", methods=["POST"])
def eliminar_materia_aprobada(padron):
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM materias_usuarios WHERE padron = %s AND materia_codigo = %s AND estado = 'aprobada'",
        (padron, materia_codigo)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return "Materia eliminada", 200


# Horarios disponibles
@perfil_usuario_bp.route("/usuario/<int:padron>/horarios-usuario", methods=["GET"])
def get_horarios_usuario(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT dia, turno FROM horarios_usuarios WHERE padron = %s", (padron,)
    )

    horarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(horarios), 200


@perfil_usuario_bp.route("/usuario/<int:padron>/editar-horarios-usuario", methods=["POST"])
def editar_horarios_usuario(padron):
    data = request.get_json()
    horarios = data.get("horarios", [])  # lista de diccionarios: {"dia": ..., "turno": ...}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM horarios_usuarios WHERE padron = %s", (padron,))
    
    for horario in horarios:
        cursor.execute(
            "INSERT INTO horarios_usuarios (padron, dia, turno) VALUES (%s, %s, %s)",
            (padron, horario["dia"], horario["turno"])
        )

    conn.commit()

    cursor.close()
    conn.close()
    return "Horarios actualizados", 200


@perfil_usuario_bp.route("/usuario/<int:padron>/grupos")
def grupos_de_usuario(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT g.grupo_id, g.nombre, g.materia_codigo, m.nombre AS materia_nombre, g.tp_terminado
    FROM grupos g
    JOIN grupos_usuarios g_u ON g.grupo_id = g_u.grupo_id
    JOIN materias m ON g.materia_codigo = m.materia_codigo
    WHERE g_u.padron = %s
    GROUP BY g.grupo_id
    """, (padron,))

    grupos = cursor.fetchall()

    # Para cada grupo, obtener los integrantes
    for grupo in grupos:
        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios gu JOIN usuarios u ON gu.padron = u.padron WHERE gu.grupo_id = %s",
            (grupo['grupo_id'],)
        )
        integrantes = cursor.fetchall()
        grupo['integrantes'] = integrantes
        grupo['cantidad_integrantes'] = len(integrantes)

    cursor.execute(
        "SELECT maximo_integrantes FROM grupos WHERE grupo_id = %s",
        (grupo['grupo_id'],)
    )
    grupo['maximo_integrantes'] = cursor.fetchone()['maximo_integrantes']

    cursor.execute(
        "SELECT dia, turno FROM horarios_grupos WHERE grupo_id = %s",
        (grupo['grupo_id'],)
    )
    horarios = cursor.fetchall()
    grupo['horarios'] = [f"{h['dia']}-{h['turno']}" for h in horarios]
        

    cursor.close()
    conn.close()
    return jsonify(grupos)




@perfil_usuario_bp.route('/usuario/<int:padron>/solicitudes-pendientes', methods=['GET'])
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
    return jsonify({"pendientes": solicitudes})







