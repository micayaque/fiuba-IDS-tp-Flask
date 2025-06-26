from flask import Blueprint, jsonify, request
from db import get_connection

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/materias", methods=["GET"])
def materias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM materias;
        """
    )

    materias = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(materias), 200


@materias_bp.route("/materias/<string:codigo>/grupos", methods=["GET"])
def grupos_por_materia(codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}

    cursor.execute("SELECT * FROM materias WHERE codigo = %s", (codigo,))
    materia = cursor.fetchone()
    data['materia'] = materia

    cursor.execute(
        """
        SELECT grupos.*
        FROM grupos
        INNER JOIN materias ON grupos.codigo_materia = materias.codigo
        WHERE grupos.codigo_materia = %s AND NOT grupos.tp_terminado
        """, (codigo,)
    )
    data['grupos'] = cursor.fetchall()

    for grupo in data['grupos']:
        cursor.execute(
            "SELECT dia, turno FROM horarios_grupos WHERE id_grupo = %s",
            (grupo['id'],)
        )
        grupo['horarios'] = cursor.fetchall()

        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios g_u JOIN usuarios u ON g_u.padron = u.padron WHERE g_u.id_grupo = %s",
            (grupo['id'],)
        )
        grupo['integrantes'] = cursor.fetchall()
        grupo['cantidad_integrantes'] = len(grupo['integrantes'])

    cursor.close()
    conn.close()

    return jsonify(data), 200


@materias_bp.route("/materias/<string:codigo>/sin-grupo", methods=["GET"])
def companierxs_sin_grupo(codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}

    cursor.execute("SELECT * FROM materias WHERE codigo = %s", (codigo,))
    data['materia'] = cursor.fetchone()

    cursor.execute("""
    SELECT u.padron, u.nombre, u.carrera
    FROM usuarios u
    JOIN materias_usuarios mu ON u.padron = mu.padron
    WHERE mu.codigo_materia = %s
    AND mu.estado = 'cursando'
    AND u.padron NOT IN (
        SELECT g_u.padron
        FROM grupos_usuarios g_u
        JOIN grupos g ON g_u.id_grupo = g.id
        WHERE g.codigo_materia = %s
    )
    """, (codigo, codigo))
    data['companierxs'] = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data), 200
