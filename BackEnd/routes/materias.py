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


@materias_bp.route("/usuario/<int:padron>/agregar-materias-cursando", methods=["POST"])
def agregar_materias_cursando(padron):
    res = request.get_json()

    materias_seleccionadas = res.get('materias_seleccionadas', [])
    nueva_materia = res.get('nueva_materia', None)
    codigo_nueva_materia = res.get('codigo_nueva_materia', None)

    conn = get_connection()
    cursor = conn.cursor()

    if nueva_materia and codigo_nueva_materia:
        cursor.execute("INSERT INTO materias (materia_codigo, nombre) VALUES (%s, %s)", (codigo_nueva_materia, nueva_materia))
        materias_seleccionadas.append(codigo_nueva_materia)

    for codigo_materia in materias_seleccionadas:
        cursor.execute("INSERT INTO materias_usuarios (padron, materia_codigo, estado) VALUES (%s, %s, 'cursando')", (padron, codigo_materia))

    conn.commit()

    cursor.close()
    conn.close()

    return "Materias cursando actualizadas", 200


@materias_bp.route("/usuario/<int:padron>/eliminar-materia-cursando", methods=["POST"])
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


@materias_bp.route("/usuario/<int:padron>/agregar-materias-aprobadas", methods=["POST"])
def agregar_materias_aprobadas(padron):
    res = request.get_json()

    materias_seleccionadas = res.get('materias_seleccionadas', [])
    nueva_materia = res.get('nueva_materia', None)
    codigo_nueva_materia = res.get('codigo_nueva_materia', None)

    conn = get_connection()
    cursor = conn.cursor()

    if nueva_materia and codigo_nueva_materia:
        cursor.execute("INSERT INTO materias (materia_codigo, nombre) VALUES (%s, %s)", (codigo_nueva_materia, nueva_materia))
        materias_seleccionadas.append(codigo_nueva_materia)

    for codigo_materia in materias_seleccionadas:
        cursor.execute("INSERT INTO materias_usuarios (padron, materia_codigo, estado) VALUES (%s, %s, 'aprobada')", (padron, codigo_materia))

    conn.commit()

    cursor.close()
    conn.close()
    return "Materias aprobadas actualizadas", 200


@materias_bp.route("/usuario/<int:padron>/eliminar-materia-aprobada", methods=["POST"])
def eliminar_materia_aprobada(padron):
    data = request.get_json()
    materia_codigo = data.get("materia_codigo")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materias_usuarios WHERE padron = %s AND materia_codigo = %s AND estado = 'aprobada'", (padron, materia_codigo))

    conn.commit()

    cursor.close()
    conn.close()
    
    return "Materia eliminada", 200
