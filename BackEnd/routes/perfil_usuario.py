from flask import Blueprint, jsonify, request, render_template
from db import get_connection

perfil_usuario_bp = Blueprint("perfil_usuario", __name__)


@perfil_usuario_bp.route("/usuario/<int:padron>", methods=["GET"])
def get_perfil_usuario(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}

    cursor.execute(
        "SELECT * FROM usuarios WHERE padron = %s", (padron,)
    )

    data['datos_usuario'] = cursor.fetchone()

    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()

    cursor.execute(
        """
        SELECT m_u.materia_codigo, m.nombre
        FROM materias_usuarios m_u
        JOIN materias m ON m_u.materia_codigo = m.materia_codigo
        WHERE m_u.padron = %s AND m_u.estado = 'cursando'
        """, (padron,)
    )
    data['materias_cursando'] = cursor.fetchall()
    codigos_cursando = {m["materia_codigo"] for m in data['materias_cursando']}
    data['materias_para_elegir_cursando'] = [m for m in materias if m['materia_codigo'] not in codigos_cursando]

    cursor.execute(
        """
        SELECT m_u.materia_codigo, m.nombre
        FROM materias_usuarios m_u
        JOIN materias m ON m_u.materia_codigo = m.materia_codigo
        WHERE m_u.padron = %s AND m_u.estado = 'aprobada'
        """, (padron,)
    )
    materias_aprobadas = cursor.fetchall()
    data['materias_aprobadas'] = materias_aprobadas
    codigos_aprobadas = {m["materia_codigo"] for m in materias_aprobadas}
    data['materias_para_elegir_aprobadas'] = [m for m in materias if m["materia_codigo"] not in codigos_aprobadas]

    cursor.execute("SELECT dia, turno FROM horarios_usuarios WHERE padron = %s", (padron,))
    horarios = cursor.fetchall()
    horarios_por_dia_usuario = {}
    for horario in horarios:
        horarios_por_dia_usuario.setdefault(horario["dia"], []).append(horario["turno"])     # agrupa a los turnos por día para mostrarlos más fácil en el html
    data['horarios_por_dia_usuario'] = horarios_por_dia_usuario

    cursor.execute("""
    SELECT g.grupo_id, g.nombre, g.materia_codigo, m.nombre AS materia_nombre, g.tp_terminado
    FROM grupos g
    JOIN grupos_usuarios g_u ON g.grupo_id = g_u.grupo_id
    JOIN materias m ON g.materia_codigo = m.materia_codigo
    WHERE g_u.padron = %s
    GROUP BY g.grupo_id
    """, (padron,))
    data['grupos'] = cursor.fetchall()

    for grupo in data['grupos']:
        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios gu JOIN usuarios u ON gu.padron = u.padron WHERE gu.grupo_id = %s",
            (grupo['grupo_id'],)
        )
        grupo['integrantes'] = cursor.fetchall()
        grupo['cantidad_integrantes'] = len(grupo['integrantes'])

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

    materias_para_select = []
    for materia in data['materias_cursando']:
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
        """, (materia['materia_codigo'], materia['materia_codigo']))
        companierxs = cursor.fetchall()
        companierxs = [c for c in companierxs if str(c["padron"]) != str(padron)]
        materias_para_select.append({
            "materia_codigo": materia["materia_codigo"],
            "nombre": materia["nombre"],
            "companierxs": companierxs
        })
    data['materias_para_select'] = materias_para_select

    cursor.close()
    conn.close()

    return jsonify(data), 200


@perfil_usuario_bp.route("/usuario/<int:padron>/editar-dato-perfil", methods=["POST"])
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


@perfil_usuario_bp.route("/usuario/<int:padron>/editar-horarios-usuario", methods=["POST"])
def editar_horarios_usuario(padron):
    data = request.get_json()
    horarios = data.get("horarios", [])  # lista de diccionarios: {"dia": [<turnos>], ...}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM horarios_usuarios WHERE padron = %s", (padron,))
    
    for horario in horarios:
        cursor.execute("INSERT INTO horarios_usuarios (padron, dia, turno) VALUES (%s, %s, %s)",(padron, horario["dia"], horario["turno"]))

    conn.commit()

    cursor.close()
    conn.close()
    return "Horarios actualizados", 200


@perfil_usuario_bp.route('/usuario/cambiar-estado-tp/<int:grupo_id>', methods=['POST'])
def cambiar_estado_tp(grupo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT tp_terminado FROM grupos WHERE grupo_id = %s", (grupo_id,))
    tp_terminado = cursor.fetchone()
    nuevo_estado = not tp_terminado['tp_terminado']

    cursor.execute("UPDATE grupos SET tp_terminado = %s WHERE grupo_id = %s", (nuevo_estado, grupo_id))

    conn.commit()

    cursor.close()
    conn.close()
    return "Estado del TP actualizado", 200