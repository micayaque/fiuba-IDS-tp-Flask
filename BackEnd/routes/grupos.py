from flask import Blueprint, jsonify, request, render_template
from db import get_connection

grupos_bp = Blueprint("grupos", __name__)

@grupos_bp.route("/grupos", methods=["GET"])
def get_grupos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT grupos.grupo_id, grupos.nombre, materias.nombre AS materia
        FROM grupos
        JOIN materias ON grupos.materia_codigo = materias.materia_codigo
        WHERE NOT grupos.tp_terminado
        """
    )    
    grupos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(grupos)

@grupos_bp.route("/agregar-grupo", methods=["POST"])
def crear_grupo():
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")
    nombre = data.get("nombre")
    maximo_integrantes = data.get("maximo_integrantes")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO grupos (materia_codigo, nombre, maximo_integrantes) VALUES (%s, %s, %s)",
        (materia_codigo, nombre, maximo_integrantes)
    )

    grupo_id = cursor.lastrowid

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