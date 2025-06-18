from flask import Flask, render_template, session, redirect, url_for, request
import requests
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

app.secret_key = 'clave-secreta'  # necesaria para usar session

API_BASE = "http://localhost:5000"

@app.route("/registrarse", methods=["POST"])
def registrarse():

    """
    Registra un usuario nuevo en la base de datos creando su perfil
    ---
    post:
        summary: Registrar usuario
        description: Crea un nuevo usuario en la base de datos con el número de padrón, contraseña y nombre completo.
        consumes:
            - application/x-www-form-urlencoded
        parameters:
            - name: padron
                in: formData
                type: string
                required: true
                description: Número de padrón del usuario
            - name: password
                in: formData
                type: string
                required: true
                description: Contraseña del usuario
            - name: nombre
                in: formData
                type: string
                required: true
                description: Nombre completo del usuario
        responses:
        200:
            description: Registro exitoso
        400:
            description: El usuario ya existe o datos inválidos
    """

    padron = request.form['padron']
    password = request.form['password']
    nombre = request.form['nombre']

    response = requests.post(f"{API_BASE}/registrarse", json={
        "padron": padron,
        "password": password,
        "nombre": nombre,
    })

    if response.status_code == 200:
        session['usuario'] = padron
        return redirect(url_for("usuario", padron=padron))
    elif response.status_code == 400 and response.text == "El usuario ya existe":
        return render_template("index.html", error="El usuario ya existe")
    else:
        return render_template("index.html", error="Error al registrar el usuario")

    
@app.route("/iniciar-sesion", methods=["POST"])
def iniciar_sesion():

    """
    Iniciar la sesión de un usuario existente
    ---
    post:
        summary: Iniciar sesión
        description: Inicia sesión con el número de padrón y contraseña del usuario, y redirige a su perfil.
        consumes:
            - application/x-www-form-urlencoded
        parameters:
            - name: padron
                in: formData
                type: string
                required: true
                description: Número de padrón del usuario
            - name: password
                in: formData
                type: string
                required: true
                description: Contraseña del usuario
        responses:
        200:
            description: Sesión iniciada correctamente
        400:
            description: Padron o contraseña incorrectos
    """

    padron = request.form['padron']
    password = request.form['password']

    response = requests.post(f"{API_BASE}/iniciar-sesion", json={
        "padron": padron,
        "password": password
    })

    if response.status_code == 200:
        session['usuario'] = padron
        return redirect(url_for("usuario", padron=padron))
    else:
        return render_template("index.html", error="Padron o contraseña incorrectos"), 400


@app.route("/cerrar-sesion", methods=["GET"])
def cerrar_sesion():

    """
    Cierra la sesión del usuario actual y redirige a la página de inicio
    ---
    get:
        summary: Cerrar sesión
        description: Elimina la sesión activa del usuario y lo redirige a la página de inicio.
        responses:
            302:
                description: Redirección a la página de inicio tras cerrar sesión.
    """
    
    session.clear()
    return redirect(url_for("inicio"))


@app.route("/", methods=["GET"])
def inicio():
     
    """
    Página de inicio
    ---
    get:
        summary: Página principal de la aplicación
        description: Muestra la página de inicio. Si el usuario tiene sesión iniciada, muestra las solicitudes pendientes.
        responses:
            200:
            description: Página de inicio renderizada correctamente
    """
     
    if session.get('usuario'):
        response = requests.get(f"{API_BASE}/usuario/{session['usuario']}/solicitudes-pendientes")
        solicitudes_pendientes = response.json().get("pendientes")
        session['notificacion'] = len(solicitudes_pendientes) > 0
    else:
        session['notificacion'] = False
        solicitudes_pendientes = []

    return render_template("index.html", solicitudes_pendientes=solicitudes_pendientes)


@app.route("/usuario/<int:padron>", methods=["GET"])
def usuario(padron):

    """
    Perfil de usuario
    ---
    get:
        summary: Ver perfil del usuario
        description: Muestra el perfil del usuario, incluyendo datos personales, materias cursando y aprobadas, horarios disponibles, los grupos que forma y sus solicitudes pendientes.
        parameters:
            - name: padron
            in: path
            type: integer
            required: true
            description: Número de padrón del usuario cuyo perfil se quiere ver
        responses:
            200:
                description: Perfil del usuario renderizado correctamente
            404:
                description: Usuario no encontrado
    """

    avatares = ["pepe.jpg", "tiger.jpg", "mulan.jpg", "jon.jpg", "lisa.jpg", "snoopy.jpg", "this_is_fine.jpg", "tom.jpg", "coraje.jpg"]

    response = requests.get(f"{API_BASE}/usuario/{padron}")     # datos del usuario: nombre, carrera, "sobre mi", avatar, color del banner del perfil
    if response.status_code == 200:
        datos_usuario = response.json()
    else:
        return "Usuario no encontrado", 404
    
    response = requests.get(f"{API_BASE}/materias")
    if response.status_code == 200:
        materias = response.json()
    else:
        materias = []

    response = requests.get(f"{API_BASE}/usuario/{padron}/materias-cursando")
    if response.status_code == 200:
        materias_cursando = response.json()
    else:
        materias_cursando = []
    codigos_cursando = {m["materia_codigo"] for m in materias_cursando}
    materias_para_elegir_cursando = [m for m in materias if m["materia_codigo"] not in codigos_cursando]

    response = requests.get(f"{API_BASE}/usuario/{padron}/materias-aprobadas")
    if response.status_code == 200:
        materias_aprobadas = response.json()
    else:
        materias_aprobadas = []
    codigos_aprobadas = {m["materia_codigo"] for m in materias_aprobadas}
    materias_para_elegir_aprobadas = [m for m in materias if m["materia_codigo"] not in codigos_aprobadas]

    response = requests.get(f"{API_BASE}/usuario/{padron}/horarios-usuario")
    if response.status_code == 200:
        horarios_usuario = response.json()
    else:
        horarios_usuario = []
    horarios_por_dia_usuario = {}
    for horario in horarios_usuario:
        horarios_por_dia_usuario.setdefault(horario["dia"], []).append(horario["turno"])     # agrupa a los turnos por día para mostrarlos más fácil en el html

    response = requests.get(f"{API_BASE}/usuario/{padron}/grupos")
    if response.status_code == 200:
        grupos = response.json()
    else:
        grupos = []

    response = requests.get(f"{API_BASE}/usuario/{padron}/solicitudes-pendientes")
    solicitudes_pendientes = response.json().get("pendientes")
    session['notificacion'] = len(solicitudes_pendientes) > 0

    materias_para_select = []
    for materia in materias_cursando:
        response = requests.get(f"{API_BASE}/materias/{materia['materia_codigo']}/companierxs-sin-grupo")
        if response.status_code == 200:
            companierxs = response.json().get("companierxs", [])
        else:
            companierxs = []
        if session.get('usuario'):
            companierxs = [c for c in companierxs if str(c["padron"]) != str(session["usuario"])]
        materias_para_select.append({
            "materia_codigo": materia["materia_codigo"],
            "nombre": materia["nombre"],
            "companierxs": companierxs
        })

    return render_template("perfil_de_usuario.html", usuario=datos_usuario, avatares=avatares, materias_cursando=materias_cursando, materias_aprobadas=materias_aprobadas, 
    materias_para_elegir_cursando=materias_para_elegir_cursando, materias_para_elegir_aprobadas=materias_para_elegir_aprobadas, horarios_por_dia_usuario=horarios_por_dia_usuario,
    grupos=grupos, solicitudes_pendientes=solicitudes_pendientes, materias_para_select=materias_para_select)


@app.route("/usuario/<int:padron>/editar-perfil", methods=["POST"])
def editar_perfil_usuario(padron):
    campo = request.form.get("campo")
    valor = request.form.get("valor")

    """
    Editar perfil de usuario
    ---
    post:
      summary: Editar perfil de usuario
      description: Permite modificar un campo específico de los datos del perfil del usuario.
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - name: padron
          in: path
          type: integer
          required: true
          description: Número de padrón del usuario cuyo perfil se va a editar
        - name: campo
          in: formData
          type: string
          required: true
          description: Nombre del campo del perfil a modificar (por ejemplo, 'nombre', 'carrera', etc.)
        - name: valor
          in: formData
          type: string
          required: true
          description: Nuevo valor para el campo especificado
      responses:
        200:
          description: Redirección al perfil del usuario si la edición fue exitosa
        400:
          description: Error al actualizar el perfil
    """

    response = requests.post(f"{API_BASE}/usuario/{padron}/editar-perfil", json={"campo": campo, "valor": valor})
    if response.status_code == 200:
        return redirect(url_for("usuario", padron=padron))
    else:
        return "Error al actualizar los datos del perfil", 400
    

@app.route("/usuario/<int:padron>/editar-materias-cursando", methods=["POST"])
def editar_materias_cursando(padron):
    materias_seleccionadas = request.form.getlist("materias")
    nueva_materia = request.form.get("nueva_materia")
    codigo_nueva_materia = request.form.get("codigo_nueva_materia")

    if nueva_materia and codigo_nueva_materia:
        requests.post(
            f"{API_BASE}/materias",
            json={"materia_codigo": codigo_nueva_materia, "nombre": nueva_materia}
        )
        materias_seleccionadas.append(codigo_nueva_materia)

    response = requests.get(f"{API_BASE}/usuario/{padron}/materias-cursando")
    if response.status_code == 200:
        materias_usuario = response.json()
    else:
        materias_usuario = []

    materias_actuales = [m["materia_codigo"] for m in materias_usuario]
    materias_a_agregar = set(materias_seleccionadas) - set(materias_actuales)

    for codigo in materias_a_agregar:
        requests.post(
            f"{API_BASE}/usuario/{padron}/agregar-materia-cursando",
            json={"materia_codigo": codigo}
        )

    return redirect(url_for("usuario", padron=padron))


@app.route("/usuario/<int:padron>/eliminar-materia-cursando", methods=["POST"])
def eliminar_materia_cursando(padron):
    materia_codigo = request.form.get("materia_codigo")

    requests.post(
        f"{API_BASE}/usuario/{padron}/eliminar-materia-cursando",
        json={"materia_codigo": materia_codigo}
    )

    return redirect(url_for("usuario", padron=padron))


@app.route("/usuario/<int:padron>/editar-materias-aprobadas", methods=["POST"])
def editar_materias_aprobadas(padron):
    materias_seleccionadas = request.form.getlist("materias")
    nueva_materia = request.form.get("nueva_materia")
    codigo_nueva_materia = request.form.get("codigo_nueva_materia")

    if nueva_materia and codigo_nueva_materia:
        requests.post(
            f"{API_BASE}/materias",
            json={"materia_codigo": codigo_nueva_materia, "nombre": nueva_materia}
        )
        materias_seleccionadas.append(codigo_nueva_materia)

    response = requests.get(f"{API_BASE}/usuario/{padron}/materias-aprobadas")
    if response.status_code == 200:
        materias_usuario = response.json()
    else:
        materias_usuario = []

    materias_actuales = [m["materia_codigo"] for m in materias_usuario]
    materias_a_agregar = set(materias_seleccionadas) - set(materias_actuales)

    for codigo in materias_a_agregar:
        requests.post(
            f"{API_BASE}/usuario/{padron}/agregar-materia-aprobada",
            json={"materia_codigo": codigo}
        )

    return redirect(url_for("usuario", padron=padron))


@app.route("/usuario/<int:padron>/eliminar-materia-aprobada", methods=["POST"])
def eliminar_materia_aprobada(padron):
    materia_codigo = request.form.get("materia_codigo")

    requests.post(
        f"{API_BASE}/usuario/{padron}/eliminar-materia-aprobada",
        json={"materia_codigo": materia_codigo}
    )

    return redirect(url_for("usuario", padron=padron))


@app.route("/usuario/<int:padron>/editar-horarios-usuario", methods=["POST"])
def editar_horarios_usuario(padron):
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    turnos = ['mañana', 'tarde', 'noche']

    horarios = []
    for dia in dias:
        for turno in turnos:
            if request.form.get(f"{dia}_{turno}"):      # si el checkbox está marcado
                horarios.append({"dia": dia, "turno": turno})

    requests.post(f"{API_BASE}/usuario/{padron}/editar-horarios-usuario", json={"horarios": horarios})
    
    return redirect(url_for("usuario", padron=padron))


@app.route("/usuario/<int:padron>/agregar-grupo", methods=["POST"])
def agregar_grupo(padron):
    materia_codigo = request.form.get("materiaGrupo")
    nombre_grupo = request.form.get("nombreGrupo")
    max_integrantes = request.form.get("cantidadMaxIntegrantes")
    padrones_str = request.form.get("padrones_integrantes", "")
    integrantes = [p for p in padrones_str.split(",") if p]

    if session.get('usuario') and session['usuario'] not in integrantes:
        integrantes.append(session['usuario'])

    response = requests.post(f"{API_BASE}/agregar-grupo", json={
        "materia_codigo": materia_codigo,
        "nombre": nombre_grupo,
        "maximo_integrantes": max_integrantes,
        "integrantes": integrantes,
        "padron_creador": padron
    })

    if response.status_code != 201:
        return "Error al crear grupo", 400
    grupo_id = response.json().get("grupo_id")

    horarios = []
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    turnos = ['mañana', 'tarde', 'noche']
    for dia in dias:
        for turno in turnos:
            if request.form.get(f"grupo_horario_{dia}_{turno}"):
                horarios.append({"dia": dia, "turno": turno})
    requests.post(f"{API_BASE}/grupos/{grupo_id}/agregar-horarios-grupo", json={"horarios": horarios})

    return redirect(url_for("usuario", padron=padron))


@app.route("/grupos", methods=["GET"])
def mostrar_grupos():
    response = requests.get(f"{API_BASE}/grupos")
    grupos = response.json()

    if session.get('usuario'):
        response = requests.get(f"{API_BASE}/usuario/{session['usuario']}/solicitudes-pendientes")
        solicitudes_pendientes = response.json().get("pendientes")
        session['notificacion'] = len(solicitudes_pendientes) > 0
    else:
        session['notificacion'] = False
        solicitudes_pendientes = []
    
    padron_usuario = session.get('usuario')
    grupos = [g for g in grupos if str(padron_usuario) not in [str(i['padron']) for i in g['integrantes']]]

    return render_template("grupos.html", grupos=grupos, solicitudes_pendientes=solicitudes_pendientes)


@app.route("/materias", methods=["GET"])
def mostrar_materias():
    response = requests.get(f"{API_BASE}/materias")
    materias = response.json()

    if session.get('usuario'):
        response = requests.get(f"{API_BASE}/usuario/{session['usuario']}/solicitudes-pendientes")
        solicitudes_pendientes = response.json().get("pendientes")
        session['notificacion'] = len(solicitudes_pendientes) > 0
    else:
        session['notificacion'] = False
        solicitudes_pendientes = []

    return render_template('materias.html', materias=materias, solicitudes_pendientes=solicitudes_pendientes)


@app.route("/materias/<string:materia_codigo>/grupos-por-materia", methods=["GET"])
def grupos_por_materia(materia_codigo):
    response = requests.get(f"{API_BASE}/materias/{materia_codigo}/grupos-por-materia")
    materia_grupos = response.json()

    if session.get('usuario'):
        response = requests.get(f"{API_BASE}/usuario/{session['usuario']}/solicitudes-pendientes")
        solicitudes_pendientes = response.json().get("pendientes")
        session['notificacion'] = len(solicitudes_pendientes) > 0
    else:
        session['notificacion'] = False
        solicitudes_pendientes = []

    padron_usuario = session.get('usuario')

    grupos_de_materia = materia_grupos["grupos"]
    grupos_filtrados = []
    for grupo in grupos_de_materia:
        integrantes_padrones = [str(i['padron']) for i in grupo['integrantes']]
        if str(padron_usuario) not in integrantes_padrones:
            grupos_filtrados.append(grupo)

    return render_template("grupos_por_materia.html", materia_codigo = materia_codigo, nombre_materia=materia_grupos["materia"], grupos=grupos_filtrados, 
                           solicitudes_pendientes=solicitudes_pendientes)


@app.route("/materias/<string:materia_codigo>/companierxs-sin-grupo", methods=["GET"])
def companierxs_sin_grupo_por_materia(materia_codigo):

    response = requests.get(f"{API_BASE}/materias/{materia_codigo}/companierxs-sin-grupo")
    
    materia_companierxs = response.json()

    materia = materia_companierxs["materia"]
    companierxs = materia_companierxs["companierxs"]

    padron_usuario = session.get('usuario')

    companierxs = [c for c in companierxs if str(c["padron"]) != str(padron_usuario)]

    return render_template("compañerxs_sin_grupo.html", materia=materia, compañerxs=companierxs)



@app.route('/solicitar-unirse-grupo/<int:grupo_id>', methods=['POST'])
def solicitar_unirse_grupo(grupo_id):
    if session.get('usuario'):
        padron = session['usuario']
        response = requests.post(f"{API_BASE}/grupos/{grupo_id}/solicitar-unirse-grupo", json={"padron_emisor": padron, "tipo": "usuario_a_grupo"})
        if response.status_code == 201:
            return redirect(request.referrer or url_for('usuario', padron=padron))
        else:
            return "Error al enviar la solicitud", 400
    else:
        return redirect(request.referrer or url_for('inicio'))


@app.route('/solicitud/<int:solicitud_id>/aceptar', methods=['POST'])
def aceptar_solicitud(solicitud_id):
    response = requests.get(f"{API_BASE}/solicitud/{solicitud_id}")
    solicitud = response.json()

    requests.post(f"{API_BASE}/solicitudes/{solicitud_id}/actualizar", 
        json={"estado": "aceptada", "materia_codigo": solicitud["materia_codigo"], "padron_emisor": solicitud["padron_emisor"],
              "grupo_id": solicitud["grupo_id"], "tipo": solicitud["tipo"], "padron_receptor": solicitud["padron_receptor"]})

    return redirect(request.referrer or url_for('usuario', padron=session["usuario"]))


@app.route('/solicitud/<int:solicitud_id>/rechazar', methods=['POST'])
def rechazar_solicitud(solicitud_id):
    response = requests.get(f"{API_BASE}/solicitud/{solicitud_id}")
    solicitud = response.json()

    requests.post(f"{API_BASE}/solicitudes/{solicitud_id}/actualizar", 
        json={"estado": "rechazada", "materia_codigo": solicitud["materia_codigo"], "padron_emisor": solicitud["padron_emisor"],
              "grupo_id": solicitud["grupo_id"], "tipo": solicitud["tipo"], "padron_receptor": solicitud["padron_receptor"]})

    return redirect(request.referrer or url_for('usuario', padron=session["usuario"]))


@app.route("/grupos/<int:grupo_id>/editar", methods=["POST"])
def editar_grupo(grupo_id):
    nombre = request.form.get("nombreGrupo")
    maximo_integrantes = request.form.get("cantidadMaxIntegrantes")
    integrantes = request.form.get("padrones_integrantes", "").split(",")

    horarios = []
    for dia in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']:
        for turno in ['mañana', 'tarde', 'noche']:
            if request.form.get(f"grupo_horario_{dia}_{turno}"):
                horarios.append({"dia": dia, "turno": turno})

    response = requests.post(f"{API_BASE}/grupos/{grupo_id}/editar", json={
        "nombre": nombre,
        "maximo_integrantes": maximo_integrantes,
        "integrantes": integrantes,
        "horarios": horarios
    })

    if response.status_code == 200:
        return redirect(url_for('usuario', padron=session['usuario']))
    else:
        return "Error al editar grupo", 400




@app.route('/enviar-solicitud-companierx/<int:padron_receptor>', methods=['POST'])
def enviar_solicitud_companierx(padron_receptor):
    if not session.get('usuario'):
        return redirect(url_for('inicio'))

    padron_emisor = session['usuario']
    materia_codigo = request.form.get('materia_codigo')

    response = requests.get(f"{API_BASE}/usuario/{padron_emisor}/grupos")
    grupos = response.json()
    grupo_materia = next((g for g in grupos if g['materia_codigo'] == materia_codigo), None)

    if grupo_materia:   # si el usuario ya esta en un grupo de esa materia
        grupo_id = grupo_materia['grupo_id']
        requests.post(f"{API_BASE}/solicitud/grupo-a-usuario", json={
            "grupo_id": grupo_id,
            "padron_emisor": padron_emisor,
            "padron_receptor": padron_receptor,
            "materia_codigo": materia_codigo
        })
    else:
        requests.post(f"{API_BASE}/solicitud/usuario-a-usuario", json={
            "padron_emisor": padron_emisor,
            "padron_receptor": padron_receptor,
            "materia_codigo": materia_codigo
        })

    return redirect(request.referrer or url_for('usuario', padron=padron_emisor))



@app.route('/usuario/<int:padron>/cambiar-estado-tp/<int:grupo_id>', methods=['POST'])
def cambiar_estado_tp(padron, grupo_id):
    grupo = requests.get(f"{API_BASE}/grupos/{grupo_id}").json()

    nuevo_estado = not grupo['tp_terminado']

    requests.post(f"{API_BASE}/grupos/{grupo_id}/cambiar-estado-tp", json={"tp_terminado": nuevo_estado})
    return redirect(url_for('usuario', padron=padron))


if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)