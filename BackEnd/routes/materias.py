from flask import Blueprint, jsonify, request
from db import get_connection

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/materias", methods=["GET"])
def get_materias_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT DISTINCT materias.materia_codigo, materias.nombre 
        FROM materias
        LEFT JOIN grupos ON materias.materia_codigo = grupos.materia_codigo
        LEFT JOIN materias_usuarios ON materias.materia_codigo = materias_usuarios.materia_codigo
        WHERE grupos.grupo_id IS NOT NULL OR materias_usuarios.padron IS NOT NULL
        """
    )

    materias = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(materias), 200


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

    if materia and companierxs:
        return jsonify({"materia": materia, "companierxs": companierxs}), 200
    else:
        return jsonify({"materia": materia, "companierxs": []}), 200


@materias_bp.route("/materias/<string:materia_codigo>/grupos-por-materia", methods=["GET"])
def grupos_por_materia(materia_codigo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        """
        SELECT grupos.*,
        materias.nombre AS nombre_materia
        FROM grupos
        INNER JOIN materias ON grupos.materia_codigo = materias.materia_codigo
        WHERE grupos.materia_codigo = %s AND NOT grupos.tp_terminado
        """, (materia_codigo,)
    )
    grupos_de_materia = cursor.fetchall()

    if grupos_de_materia:
        nombre_materia = grupos_de_materia[0]["nombre"]
    else:
        cursor.execute("SELECT nombre FROM materias WHERE materia_codigo = %s", (materia_codigo,))
        materia = cursor.fetchone()
        nombre_materia = materia["nombre"] if materia else ""

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

    if grupos_de_materia:
        return jsonify({ "materia": nombre_materia, "grupos": grupos_de_materia }), 200
    else:
        return jsonify({ "materia": nombre_materia, "grupos": [] }), 200

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