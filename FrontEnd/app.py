from flask import Flask, render_template, session, redirect, url_for, request
import requests

app = Flask(__name__)

app.secret_key = 'clave-secreta'  # necesaria para usar session

API_BASE = "http://localhost:5000"

@app.route("/registrarse", methods=["POST"])
def registrarse():
    padron = request.form['padron']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    response = requests.post(f"{API_BASE}/registrarse", json={
        "padron": padron,
        "password": password,
        "nombre": nombre,
        "apellido": apellido
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

@app.route("/perfil_de_usuario")
def perfil_de_usuario():
    return f"Bienvenido al perfil de {session['usuario']}"  # muestra el perfil del usuario a través del botón "Mi perfil"

@app.route("/grupos")
def mostrar_grupos():
    response = requests.get(f"{API_BASE}/grupos")
    grupos = response.json()
    return render_template("grupos.html", grupos=grupos)

@app.route("/materias")
def mostrar_materias():
    response = requests.get(f"{API_BASE}/materias")
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


@app.route("/usuario/<int:padron>")
def usuario(padron):
    avatares = ["pepe.jpg", "tiger.jpg", "mulan.jpg", "jon.jpg", "lisa.jpg", "snoopy.jpg", "this_is_fine.jpg", "tom.jpg", "coraje.jpg"]
        
    response = requests.get(f"{API_BASE}/usuario/{padron}")
    usuario = response.json()
    return render_template("perfil_de_usuario.html", usuario=usuario, avatares=avatares)

if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)