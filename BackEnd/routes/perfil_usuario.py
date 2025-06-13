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