from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import requests

app = Flask(__name__)

app.secret_key = 'clave-secreta'  # necesaria para usar session

API_BASE = "http://localhost:5000"

@app.route("/registrarse", methods=["POST"])
def registrarse():
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
        return redirect(url_for("inicio"))
    elif response.status_code == 400 and response.text == "El usuario ya existe":
        return render_template("index.html", error="El usuario ya existe")
    else:
        return render_template("index.html", error="Error al registrar el usuario")

    
@app.route("/iniciar-sesion", methods=["POST"])
def iniciar_sesion():
    padron = request.form['padron']
    password = request.form['password']

    response = requests.post(f"{API_BASE}/iniciar-sesion", json={
        "padron": padron,
        "password": password
    })

    if response.status_code == 200:
        session['usuario'] = padron
        return redirect(url_for("inicio"))
    else:
        return render_template("index.html", error="Padron o contraseña incorrectos")


@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("inicio"))


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/usuario/<int:padron>")
def usuario(padron):
    avatares = ["pepe.jpg", "tiger.jpg", "mulan.jpg", "jon.jpg", "lisa.jpg", "snoopy.jpg", "this_is_fine.jpg", "tom.jpg", "coraje.jpg"]
        
    response = requests.get(f"{API_BASE}/usuario/{padron}")
    usuario = response.json()

    materias = requests.get(f"{API_BASE}/materias").json()

    response = requests.get(f"{API_BASE}/usuario/{padron}/materias-cursando")
    if response.status_code == 200:
        materias_cursando = response.json()
    else:
        materias_cursando = []

    codigos_cursando = {m["materia_codigo"] for m in materias_cursando}
    materias_para_elegir = [m for m in materias if m["materia_codigo"] not in codigos_cursando]

    # grupos = requests.get(f"{API_BASE}/grupos").json()

    return render_template("perfil_de_usuario.html", usuario=usuario, avatares=avatares, materias_cursando=materias_cursando, materias_para_elegir=materias_para_elegir)


@app.route("/usuario/<int:padron>/editar-perfil", methods=["POST"])
def editar_perfil_usuario(padron):
    campo = request.form.get("campo")
    valor = request.form.get("valor")
    # Envía el request al backend como JSON
    response = requests.post(
        f"{API_BASE}/usuario/{padron}/editar-perfil",
        json={"campo": campo, "valor": valor}
    )
    # Puedes manejar la respuesta JSON si lo deseas
    if response.status_code == 200:
        return redirect(url_for("usuario", padron=padron))
    else:
        # Puedes mostrar un mensaje de error si quieres
        return "Error al actualizar el perfil", 400
    

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
    materias_a_eliminar = set(materias_actuales) - set(materias_seleccionadas)

    for codigo in materias_a_agregar:
        requests.post(
            f"{API_BASE}/usuario/{padron}/agregar-materia-cursando",
            json={"materia_codigo": codigo}
        )

    for codigo in materias_a_eliminar:
        requests.post(
            f"{API_BASE}/usuario/{padron}/eliminar-materia",
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


@app.route("/grupos")
def mostrar_grupos():
    response = requests.get(f"{API_BASE}/grupos")
    grupos = response.json()
    return render_template("grupos.html", grupos=grupos)


@app.route("/materias")
def mostrar_materias():
    response = requests.get(f"{API_BASE}/materias-grupos")
    materias = response.json()
    return render_template('materias.html', materias=materias)


@app.route("/materias/<string:materia_codigo>/grupos")
def grupos_por_materia(materia_codigo):
    response = requests.get(f"{API_BASE}/materias/{materia_codigo}/grupos")
    grupos = response.json()
    return render_template("grupos_por_materia.html", nombre_materia=grupos[0]["nombre_materia"], materia_codigo=grupos[0]["materia_codigo"], grupos=grupos)


@app.route("/materias/<int:codigo_materia>/companieros-sin-grupo")
def companieros_sin_grupo_por_materia(materia_codigo):
    materia = None
    for m in materias:
        if m["codigo_materia"] == materia_codigo:
            materia = m
            break

    compañeros_sin_grupo = [
        {"padron": 543211, "nombre": "Compañerx 1"},
        {"padron": 543212, "nombre": "Compañerx 2"},
        {"padron": 543213, "nombre": "Compañerx 3"},
        {"padron": 543214, "nombre": "Compañerx 4"},
    ]

    return render_template("compañerxs_sin_grupo.html", materia=materia, compañeros=compañeros_sin_grupo)


if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)