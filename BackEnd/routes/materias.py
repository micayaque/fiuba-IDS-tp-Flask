from flask import Blueprint, jsonify, request
from db import get_connection

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/materias", methods=["GET"])
def materias():
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


@materias_bp.route("/materias", methods=["POST"])
def agregar_materia():
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")
    nombre = data.get("nombre")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO materias (materia_codigo, nombre) VALUES (%s, %s)", (materia_codigo, nombre))
    
    conn.commit()
    
    cursor.close()
    conn.close()

    return "Materia agregada", 200

