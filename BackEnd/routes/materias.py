from flask import Blueprint, jsonify, request
from db import get_connection

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/materias", methods=["GET"])
def get_materias_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DISTINCT m.* FROM materias m JOIN materias_usuarios m_u ON m.materia_codigo = m_u.materia_codigo WHERE m_u.estado = 'cursando'
    """)

    materias = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(materias)


@materias_bp.route("/materias-grupos", methods=["GET"])
def get_materias_grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT DISTINCT materias.materia_codigo, materias.nombre 
        FROM materias
        INNER JOIN grupos ON materias.materia_codigo = grupos.materia_codigo
        """)
    materias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(materias)

@materias_bp.route("/materias", methods=["POST"])
def agregar_materia():
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")
    nombre = data.get("nombre")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO materias (materia_codigo, nombre) VALUES (%s, %s)",
        (materia_codigo, nombre)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    return "Materia agregada", 200


@materias_bp.route("/materias/<string:materia_codigo>/grupos-por-materia", methods=["GET"])
def grupos_por_materia(materia_codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT nombre FROM materias WHERE materia_codigo = %s", (materia_codigo,))

    materia = cursor.fetchone()
    nombre_materia = materia["nombre"]

    cursor.execute(
        """
        SELECT grupos.*
        FROM grupos
        WHERE grupos.materia_codigo = %s AND NOT grupos.tp_terminado
        """, (materia_codigo,)
    )
    grupos_de_materia = cursor.fetchall()

    for grupo in grupos_de_materia:
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
    return jsonify({ "nombre_materia": nombre_materia, "grupos": grupos_de_materia })


@materias_bp.route("/materias/<string:materia_codigo>/companierxs-sin-grupo", methods=["GET"])
def companierxs_sin_grupo(materia_codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

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
    companierxs = cursor.fetchall()

    cursor.execute("SELECT * FROM materias WHERE materia_codigo = %s", (materia_codigo,))
    materia = cursor.fetchone()

    cursor.close()
    conn.close()
    return jsonify({"materia": materia, "companierxs": companierxs})