from flask import Blueprint, jsonify, request
from db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route('/usuarios', methods=['POST'])
def registrarse():
    data = request.get_json()
    padron = data['padron']
    password = data['password']
    nombre = data['nombre']
    apellido = data['apellido']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE padron = %s", (padron,))
    usuario = cursor.fetchone()
    if usuario:
        cursor.close()
        conn.close()
        return jsonify({"error": "El usuario ya existe"}), 400

    cursor.execute("INSERT INTO usuarios (padron, contrasena, nombre, apellido) VALUES (%s, %s, %s, %s)", (padron, password, nombre, apellido))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Error al registrar el usuario"}), 400

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Usuario registrado correctamente"}), 201


@usuarios_bp.route("/usuarios/<int:padron>", methods=["GET"])
def perfil(padron):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = {}

    cursor.execute("SELECT * FROM usuarios WHERE padron = %s", (padron,))
    data['datos_usuario'] = cursor.fetchone()

    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()

    cursor.execute(
        """
        SELECT m_u.codigo_materia, m.nombre
        FROM materias_usuarios m_u
        JOIN materias m ON m_u.codigo_materia = m.codigo
        WHERE m_u.padron = %s AND m_u.estado = 'cursando'
        """, (padron,)
    )
    data['materias_cursando'] = cursor.fetchall()
    codigos_cursando = {m["codigo_materia"] for m in data['materias_cursando']}
    data['materias_para_elegir_cursando'] = [m for m in materias if m['codigo'] not in codigos_cursando]

    cursor.execute(
        """
        SELECT m_u.codigo_materia, m.nombre
        FROM materias_usuarios m_u
        JOIN materias m ON m_u.codigo_materia = m.codigo
        WHERE m_u.padron = %s AND m_u.estado = 'aprobada'
        """, (padron,)
    )
    materias_aprobadas = cursor.fetchall()
    data['materias_aprobadas'] = materias_aprobadas
    codigos_aprobadas = {m["codigo_materia"] for m in materias_aprobadas}
    data['materias_para_elegir_aprobadas'] = [m for m in materias if m["codigo"] not in codigos_aprobadas]

    cursor.execute("SELECT dia, turno FROM horarios_usuarios WHERE padron = %s", (padron,))
    horarios = cursor.fetchall()
    horarios_por_dia_usuario = {}
    for horario in horarios:
        horarios_por_dia_usuario.setdefault(horario["dia"], []).append(horario["turno"])     # agrupa a los turnos por día para mostrarlos más fácil en el html
    data['horarios_por_dia_usuario'] = horarios_por_dia_usuario

    cursor.execute("""
    SELECT g.id, g.nombre, g.codigo_materia, m.nombre AS materia_nombre, g.tp_terminado
    FROM grupos g
    JOIN grupos_usuarios g_u ON g.id = g_u.id_grupo
    JOIN materias m ON g.codigo_materia = m.codigo
    WHERE g_u.padron = %s
    GROUP BY g.id
    """, (padron,))
    data['grupos'] = cursor.fetchall()

    for grupo in data['grupos']:
        cursor.execute(
            "SELECT u.padron, u.nombre FROM grupos_usuarios gu JOIN usuarios u ON gu.padron = u.padron WHERE gu.id_grupo = %s",
            (grupo['id'],)
        )
        grupo['integrantes'] = cursor.fetchall()
        grupo['cantidad_integrantes'] = len(grupo['integrantes'])

        cursor.execute(
            "SELECT maximo_integrantes FROM grupos WHERE id = %s",
            (grupo['id'],)
        )
        grupo['maximo_integrantes'] = cursor.fetchone()['maximo_integrantes']

        cursor.execute(
            "SELECT dia, turno FROM horarios_grupos WHERE id_grupo = %s",
            (grupo['id'],)
        )
        horarios = cursor.fetchall()
        grupo['horarios'] = [f"{h['dia']}-{h['turno']}" for h in horarios]

    materias_para_select = []
    cursor.execute("""
            SELECT m.codigo, m.nombre FROM materias m JOIN materias_usuarios m_u ON m.codigo = m_u.codigo_materia
            WHERE m_u.padron = %s AND m_u.estado = 'cursando' AND m.codigo NOT IN (SELECT codigo_materia FROM grupos_usuarios WHERE padron = %s)
    """, (padron, padron))
    materias = cursor.fetchall()
 
    for materia in materias:
        cursor.execute("""
            SELECT u.padron, u.nombre FROM usuarios u JOIN materias_usuarios m_u ON u.padron = m_u.padron
            WHERE m_u.codigo_materia = %s AND m_u.estado = 'cursando' AND u.padron NOT IN (SELECT padron FROM grupos_usuarios WHERE codigo_materia = %s)
        """, (materia['codigo'], materia['codigo']))
        companierxs = cursor.fetchall()
        companierxs = [c for c in companierxs if str(c["padron"]) != str(padron)]
        materias_para_select.append({
            "materia_codigo": materia["codigo"],
            "nombre": materia["nombre"],
            "companierxs": companierxs
        })
    data['materias_para_select'] = materias_para_select

    cursor.close()
    conn.close()

    return jsonify(data), 200 


@usuarios_bp.route("/usuarios/<int:padron>", methods=["PATCH"])
def editar_datos_usuario(padron):
    data = request.get_json()
    campo = data.get("campo")
    valor = data.get("valor")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE usuarios SET {campo} = %s WHERE padron = %s", (valor, padron))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "No hubo cambios"}), 200

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Perfil actualizado"}), 200


@usuarios_bp.route("/usuarios/<int:padron>/horarios", methods=["PATCH"])
def editar_horarios(padron):
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


@usuarios_bp.route("/usuarios/<int:padron>/materias", methods=["POST"])
def agregar_materias(padron):
    res = request.get_json()
    materias_seleccionadas = res.get('materias_seleccionadas', [])
    nueva_materia = res.get('nueva_materia', None)
    codigo_nueva_materia = res.get('codigo_nueva_materia', None)
    estado_materia = res.get('estado_materia')

    conn = get_connection()
    cursor = conn.cursor()

    if nueva_materia and codigo_nueva_materia:
        cursor.execute("INSERT INTO materias (codigo, nombre) VALUES (%s, %s)", (codigo_nueva_materia, nueva_materia))
        materias_seleccionadas.append(codigo_nueva_materia)
 
    for codigo_materia in materias_seleccionadas:
        if estado_materia == 'cursando':
            cursor.execute("SELECT * FROM materias_usuarios WHERE padron = %s AND codigo_materia = %s AND estado = 'aprobada'", (padron, codigo_materia))
            if cursor.fetchone():
                cursor.execute("DELETE FROM materias_usuarios WHERE padron = %s AND codigo_materia = %s AND estado = 'aprobada'", (padron, codigo_materia))
            cursor.execute("INSERT INTO materias_usuarios (padron, codigo_materia, estado) VALUES (%s, %s, 'cursando')", (padron, codigo_materia))
        else:
            cursor.execute("SELECT * FROM materias_usuarios WHERE padron = %s AND codigo_materia = %s AND estado = 'cursando'", (padron, codigo_materia))
            if cursor.fetchone():
                cursor.execute("DELETE FROM materias_usuarios WHERE padron = %s AND codigo_materia = %s AND estado = 'cursando'", (padron, codigo_materia))
            cursor.execute("INSERT INTO materias_usuarios (padron, codigo_materia, estado) VALUES (%s, %s, 'aprobada')", (padron, codigo_materia))

    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Materias cursando actualizadas"}), 200


@usuarios_bp.route("/usuario/<int:padron>/materias/<materia_codigo>", methods=["DELETE"])
def eliminar_materia(padron, materia_codigo):
    estado_materia = request.get_json().get("estado_materia")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM materias_usuarios WHERE padron = %s AND codigo_materia = %s AND estado = %s",
        (padron, materia_codigo, estado_materia)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Materia eliminada"}), 200