from flask import Blueprint, jsonify, request, render_template
from db import get_connection

perfil_usuario_bp = Blueprint("perfil_usuario", __name__)

@perfil_usuario_bp.route('/usuarios', methods=['POST'])
def registrarse():
    data = request.get_json()
    padron = data['padron']
    password = data['password']
    nombre = data['nombre']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE padron = %s", (padron,))
    usuario = cursor.fetchone()
    if usuario:
        cursor.close()
        conn.close()
        return jsonify({"error": "El usuario ya existe"}), 400

    cursor.execute("INSERT INTO usuarios (padron, contrasena, nombre) VALUES (%s, %s, %s)", (padron, password, nombre))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Error al registrar el usuario"}), 400

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Usuario registrado correctamente"}), 200


@perfil_usuario_bp.route("/usuarios/<int:padron>", methods=["GET"])
def perfil_usuario(padron):
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
    cursor.execute("""
            SELECT m.materia_codigo, m.nombre FROM materias m JOIN materias_usuarios m_u ON m.materia_codigo = m_u.materia_codigo
            WHERE m_u.padron = %s AND m_u.estado = 'cursando' AND m.materia_codigo NOT IN (SELECT materia_codigo FROM grupos_usuarios WHERE padron = %s)
        """, (padron, padron))
    materias = cursor.fetchall()
    for materia in materias:
        cursor.execute("""
            SELECT u.padron, u.nombre FROM usuarios u JOIN materias_usuarios m_u ON u.padron = m_u.padron
            WHERE m_u.materia_codigo = %s AND m_u.estado = 'cursando' AND u.padron NOT IN (SELECT padron FROM grupos_usuarios WHERE materia_codigo = %s)
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


@perfil_usuario_bp.route("/usuarios/<int:padron>", methods=["PATCH"])
def editar_perfil_usuario(padron):
    data = request.get_json()
    campo = data.get("campo")
    valor = data.get("valor")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE usuarios SET {campo} = %s WHERE padron = %s", (valor, padron))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Error al actualizar el perfil"}), 400

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Perfil actualizado"}), 200


@perfil_usuario_bp.route("/usuarios/<int:padron>/horarios", methods=["PATCH"])
def editar_horarios_usuario(padron):
    data = request.get_json()
    horarios = data.get("horarios", [])  # lista de diccionarios: {"dia": [<turno>], ...}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM horarios_usuarios WHERE padron = %s", (padron,))
    
    for horario in horarios:
        cursor.execute("INSERT INTO horarios_usuarios (padron, dia, turno) VALUES (%s, %s, %s)",(padron, horario["dia"], horario["turno"]))

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Horarios actualizados"}), 200

