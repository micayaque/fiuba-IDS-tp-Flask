from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import requests
from flasgger import Swagger

from flask_mail import Mail, Message
from config_mail import MAIL_SETTINGS

app = Flask(__name__)
swagger = Swagger(app)

app.config.update(MAIL_SETTINGS)
mail = Mail(app)

app.secret_key = 'clave-secreta'  # necesaria para usar session

API_BASE = "http://localhost:5000"

@app.errorhandler(500)
def error_interno_servidor(error):
    return render_template('errores.html'), 500

@app.errorhandler(404)
def error404(error):
    return render_template("errores.html"), 404


@app.route("/inicio-sesion", methods=["POST"])
def iniciar_sesion():
    padron = request.form['padron']
    password = request.form['password']

    if not padron.isdigit():
        return redirect(url_for('inicio', error="El padrón solo puede ser un número"))

    response = requests.post(f"{API_BASE}/sesiones", json={ "padron": padron, "password": password })

    if response.status_code == 200:
        session['usuario'] = padron
        return usuario(padron)
    else:
        return redirect(url_for('inicio', error="Padrón o contraseña incorrectos"))


@app.route("/cerrar-sesion", methods=["POST"])
def cerrar_sesion():
    session.clear()
    return redirect(url_for("inicio"))



@app.route("/usuarios", methods=["POST"])
def registrarse():
    padron = request.form['padron']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    if not padron.isdigit():
        return redirect(url_for('inicio', error="El padrón solo puede ser un número"))

    response = requests.post(f"{API_BASE}/usuarios", json={ "padron": padron, "password": password, "nombre": nombre, "apellido": apellido })
    res = response.json()

    if response.status_code == 201:
        session['usuario'] = padron
        return usuario(padron)
    elif res.get("error") == "El usuario ya existe":
        return inicio(error="El usuario ya existe")
    else:
        return inicio(error="Error al registrar el usuario")


@app.route("/usuarios/<int:padron>", methods=["GET"])
def usuario(padron):
    data = requests.get(f"{API_BASE}/usuarios/{padron}").json()    
    data['avatares'] = ["pepe.jpg", "tiger.jpg", "mulan.jpg", "jon.jpg", "lisa.jpg", "snoopy.jpg", "this_is_fine.jpg", "tom.jpg", "coraje.jpg"]
    data['solicitudes_pendientes'] = solicitudes_pendientes(padron)

    session['notificacion'] = len(data['solicitudes_pendientes']) > 0
 
    return render_template("perfil_de_usuario.html", data=data, error=request.args.get("error"))


@app.route("/usuarios/<int:padron>/editar-perfil", methods=["POST"])
def editar_perfil_usuario(padron):
    if 'nombre' in request.form and 'apellido' in request.form:
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        
        requests.patch(f"{API_BASE}/usuarios/{padron}", 
                                       json={"campo": "nombre", "valor": nombre})        
        requests.patch(f"{API_BASE}/usuarios/{padron}", 
                                         json={"campo": "apellido", "valor": apellido})
    else:
        campo = request.form.get("campo")
        valor = request.form.get("valor")
        
        requests.patch(f"{API_BASE}/usuarios/{padron}", 
                                json={"campo": campo, "valor": valor})
    return usuario(padron)


@app.route("/usuarios/<int:padron>/editar-horarios", methods=["POST"])
def editar_horarios_usuario(padron):
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    turnos = ['mañana', 'tarde', 'noche']
    horarios = []

    for dia in dias:
        for turno in turnos:
            if request.form.get(f"{dia}_{turno}"):
                horarios.append({"dia": dia, "turno": turno})

    requests.patch(f"{API_BASE}/usuarios/{padron}/horarios", json={"horarios": horarios})
    
    return usuario(padron)


@app.route("/usuario/<int:padron>/agregar-materias-cursando", methods=["POST"])
def agregar_materias_cursando(padron):
    materias_seleccionadas = request.form.getlist("materias")
    nueva_materia = request.form.get("nueva_materia")
    codigo_nueva_materia = request.form.get("codigo_nueva_materia")

    requests.post(f"{API_BASE}/usuarios/{padron}/materias",
        json={"materias_seleccionadas": materias_seleccionadas, "nueva_materia": nueva_materia, 
              "codigo_nueva_materia": codigo_nueva_materia, "estado_materia": "cursando"})
 
    return usuario(padron)


@app.route("/usuario/<int:padron>/eliminar-materia-cursando", methods=["POST"])
def eliminar_materia_cursando(padron):
    materia_codigo = request.form.get("materia_codigo")

    requests.delete(f"{API_BASE}/usuario/{padron}/materias/{materia_codigo}", json={"estado_materia": "cursando"})

    return usuario(padron)


@app.route("/usuario/<int:padron>/agregar-materias-aprobadas", methods=["POST"])
def agregar_materias_aprobadas(padron):
    materias_seleccionadas = request.form.getlist("materias")
    nueva_materia = request.form.get("nueva_materia")
    codigo_nueva_materia = request.form.get("codigo_nueva_materia")

    requests.post(f"{API_BASE}/usuarios/{padron}/materias",
        json={"materias_seleccionadas": materias_seleccionadas, "nueva_materia": nueva_materia, 
              "codigo_nueva_materia": codigo_nueva_materia, "estado_materia": "aprobada"})

    return usuario(padron)



@app.route("/usuario/<int:padron>/eliminar-materia-aprobada", methods=["POST"])
def eliminar_materia_aprobada(padron):
    materia_codigo = request.form.get("materia_codigo")

    requests.delete(f"{API_BASE}/usuario/{padron}/materias/{materia_codigo}", json={"estado_materia": "aprobada"})

    return usuario(padron)


@app.route("/materias/<string:codigo>/sin-grupo", methods=["GET"])
def usuarios_sin_grupo_por_materia(codigo):
    response = requests.get(f"{API_BASE}/materias/{codigo}/sin-grupo")    
    data = response.json()

    padron_usuario = session.get('usuario')

    data['companierxs'] = [c for c in data["companierxs"] if str(c["padron"]) != str(padron_usuario)]

    if not data['companierxs']:
        error = "No hay compañerxs buscando grupo en este momento. Busca un grupo formado y pide para unirte."
    else:
        error = ""

    return render_template("compañerxs_sin_grupo.html", data=data, error=error)


@app.route("/materias", methods=["GET"])
def materias():
    response = requests.get(f"{API_BASE}/materias")
    data = {}
    data['materias'] = response.json()

    data['solicitudes_pendientes'] = solicitudes_pendientes(session.get('usuario'))
    session['notificacion'] = len(data['solicitudes_pendientes']) > 0

    return render_template('materias.html', data=data)


@app.route("/materias/<string:codigo>/grupos", methods=["GET"])
def grupos_por_materia(codigo):
    response = requests.get(f"{API_BASE}/materias/{codigo}/grupos")
    data = response.json()

    padron_usuario = session.get('usuario')

    grupos_de_materia = data["grupos"]
    grupos_filtrados = []
    for grupo in grupos_de_materia:
        integrantes_padrones = [str(i['padron']) for i in grupo['integrantes']]
        if str(padron_usuario) not in integrantes_padrones:
            grupos_filtrados.append(grupo)
    data['grupos'] = grupos_filtrados

    data['solicitudes_pendientes'] = solicitudes_pendientes(session.get('usuario'))
    session['notificacion'] = len(data['solicitudes_pendientes']) > 0

    if not data['grupos']:
        error = "Aún no hay grupos formados para esta materia. Podes ver a los compañeros sin grupo para formar uno."
    else:
        error = ""

    return render_template("grupos_por_materia.html", data=data, error=error)




@app.route("/grupos", methods=["GET"])
def grupos():
    response = requests.get(f"{API_BASE}/grupos")
    data = response.json()

    data['solicitudes_pendientes'] = solicitudes_pendientes(session.get('usuario'))
    session['notificacion'] = len(data['solicitudes_pendientes']) > 0

    padron_usuario = session.get('usuario')
    grupos_filtrados = []
    for grupo in data['grupos']:
        padrones = [str(integrante['padron']) for integrante in grupo['integrantes']]
        if str(padron_usuario) not in padrones:
            grupos_filtrados.append(grupo)
    data['grupos'] = grupos_filtrados

    if not data['grupos']:
        error = "No hay grupos disponibles. Crea el tuyo o invita a gente que no tenga en la sección materias."
    else:
        error = ""
    
    return render_template("grupos.html", data=data, error=error)


@app.route("/grupos/<int:padron>/agregar-grupo", methods=["POST"])
def agregar_grupo(padron):
    materia_codigo = request.form.get("materiaGrupo")
    nombre_grupo = request.form.get("nombreGrupo")
    padrones_str = request.form.get("padrones_integrantes", "")
    integrantes = [p for p in padrones_str.split(",") if p]
    max_integrantes = request.form.get("cantidadMaxIntegrantes")
    if not max_integrantes:
        max_integrantes = 10
    elif len(integrantes) > int(max_integrantes):
        return redirect(url_for("usuario", padron=padron, error="La cantidad de integrantes supera el máximo permitido"))

    if session.get('usuario') and session['usuario'] not in integrantes:
        integrantes.append(session['usuario'])

    horarios = []
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    turnos = ['mañana', 'tarde', 'noche']
    for dia in dias:
        for turno in turnos:
            if request.form.get(f"grupo_horario_{dia}_{turno}"):
                horarios.append({"dia": dia, "turno": turno})

    response = requests.post(f"{API_BASE}/grupos", json={ "materia_codigo": materia_codigo, "nombre": nombre_grupo, "maximo_integrantes": max_integrantes,
        "integrantes": integrantes, "padron_creador": padron, "horarios": horarios})
    
    if response.status_code == 400:
        error = response.json().get("error")
        return redirect(url_for("usuario", padron=padron, error=error))

    return usuario(padron)


@app.route("/grupos/<int:grupo_id>/editar", methods=["POST"])
def editar_grupo(grupo_id):
    nombre = request.form.get("nombreGrupo")
    integrantes = request.form.get("padrones_integrantes", "").split(",")
    maximo_integrantes = request.form.get("editarCantidadMaxIntegrantes")
    padron_editor = session.get('usuario')

    horarios = []
    for dia in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']:
        for turno in ['mañana', 'tarde', 'noche']:
            if request.form.get(f"grupo_horario_{dia}_{turno}"):
                horarios.append({"dia": dia, "turno": turno})

    response = requests.patch(f"{API_BASE}/grupos/{grupo_id}", json={ "nombre": nombre, "maximo_integrantes": maximo_integrantes,
        "integrantes": integrantes, "horarios": horarios, "padron_editor": padron_editor
    })

    if response.status_code == 400:
        error = response.json().get("error")
        return redirect(url_for("usuario", padron=padron_editor, error=error))

    return usuario(padron_editor)


@app.route('/grupos/<int:grupo_id>/estado-tp/', methods=['POST'])
def cambiar_estado_tp(grupo_id):
    requests.patch(f"{API_BASE}/grupo/{grupo_id}/estado-tp")

    return usuario(session.get('usuario'))



@app.route("/solicitudes/<int:padron>/solicitudes-pendientes", methods=["GET"])
def solicitudes_pendientes(padron):
    if padron:
        response = requests.get(f"{API_BASE}/solicitudes/{padron}")
        data = response.json()
        solicitudes_pendientes = data.get("solicitudes_pendientes", [])
    else:
        solicitudes_pendientes = []
    return solicitudes_pendientes


@app.route('/solicitudes/<int:solicitud_id>/aceptar', methods=['POST'])
def aceptar_solicitud(solicitud_id):

    requests.patch(f"{API_BASE}/solicitudes/{solicitud_id}", json={"estado": "aceptada"})

    return usuario(session.get("usuario"))
    

@app.route('/solicitudes/<int:solicitud_id>/rechazar', methods=['POST'])
def rechazar_solicitud(solicitud_id):

    requests.patch(f"{API_BASE}/solicitudes/{solicitud_id}", 
        json={"estado": "rechazada"})

    return usuario(session.get("usuario"))


@app.route('/solicitudes/<int:grupo_id>', methods=['POST'])
def solicitar_unirse_grupo(grupo_id):
    if session.get('usuario'):
        padron = session['usuario']
        response = requests.post(f"{API_BASE}/solicitudes/grupos/{grupo_id}", json={"padron_emisor": padron, "tipo": "usuario_a_grupo"})
        if response.status_code == 201:
            return redirect(request.referrer or url_for('usuario', padron=padron))
        elif response.status_code == 400:
            error = response.json().get("error")
            return redirect(url_for('usuario', padron=padron, error=error))
        else:
            return "Error al enviar la solicitud", 400
    else:
        return inicio(error="Debes iniciar sesión para enviar solicitudes")


@app.route('/solicitudes/enviar-solicitud-companierx/<string:materia_codigo>/<int:padron_emisor>/<int:padron_receptor>', methods=['POST'])
def enviar_solicitud_companierx(materia_codigo, padron_emisor, padron_receptor):
    if not session.get('usuario'):
        return inicio(error="Debes iniciar sesión para enviar solicitudes")

    response = requests.post(f"{API_BASE}/solicitudes/usuarios/{padron_receptor}", 
        json={"materia_codigo": materia_codigo, "padron_emisor": padron_emisor})

    if response.status_code == 201:
        return usuario(padron_emisor)
    else:
        return redirect(url_for('usuarios_sin_grupo_por_materia', codigo=materia_codigo))



@app.route("/", methods=["GET"])
def inicio():
    response = requests.get(f"{API_BASE}/cantidad-grupos")
    data = response.json() 
    data['solicitudes_pendientes'] = solicitudes_pendientes(session.get('usuario'))
    session['notificacion'] = len(data['solicitudes_pendientes']) > 0
    # session['usuario'] = session.get('usuario')

    error = request.args.get("error")

    return render_template("index.html", data=data, error=error)


@app.route('/contacto', methods=['POST'])
def contacto():
    email = request.form['email']
    mensaje = request.form['mensaje']

    destinatarios = ['myaque@fi.uba.ar']

    msg = Message(
        subject='Nuevo mensaje del sitio',
        recipients=destinatarios,
        body=f"Email: {email}\nMensaje:\n{mensaje}",
        reply_to=email
    )
    
    try:
        mail.send(msg)
        return redirect(url_for('inicio', error="¡Mensaje enviado!"))
    except:
        return redirect(url_for('inicio', error="Ocurrió un error al enviar el mensaje"))



if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)