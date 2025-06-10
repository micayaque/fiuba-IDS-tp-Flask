from flask import Blueprint, jsonify, request
from db import get_connection

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/materias")
def get_materias():
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


@materias_bp.route("/materias/<string:materia_codigo>/grupos")
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
    cursor.close()
    conn.close()
    
    return jsonify(grupos_de_materia)