from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)

app.secret_key = 'clave-secreta'  # necesaria para usar session

@app.route("/")
def inicio():
    return render_template("index.html")

# endpoint para prueba de iniciar sesión (sin validación de usuario) 
@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    session["usuario"] = request.form.get("padron")  # obtenemos y guardamos el padrón ingresado por el usuario para saber quién está (si hay alguien) con la sesión iniciada
    next_url = request.form.get("next")              # obtenemos la URL en la que estaba el usuario antes de iniciar sesión
    return redirect(next_url)                        # redirige a dicha URL

@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.pop("usuario", None)                    # para cerrar la sesión, eliminamos al usuario de session
    return redirect(url_for("inicio"))                # volvemos a la página principal

@app.route("/perfil_de_usuario")
def perfil_de_usuario():
    return f"Bienvenido al perfil de {session['usuario']}"  # muestra el perfil del usuario a través del botón "Mi perfil"

@app.route("/materias")
def mostrar_materias():
    materias = [
        {"codigo_materia": 1, "nombre": "Fundamentos de la programación"},
        {"codigo_materia": 2, "nombre": "Introducción al desarrollo de software"},
        {"codigo_materia": 3, "nombre": "Organización del computador"},
        {"codigo_materia": 4, "nombre": "Probabilidad y estadística"},
        {"codigo_materia": 5, "nombre": "Sistemas operativos"},
        {"codigo_materia": 6, "nombre": "Paradigmas de programación"},
        {"codigo_materia": 7, "nombre": "Base de datos"},
        {"codigo_materia": 8, "nombre": "Ciencia de datos"},
        {"codigo_materia": 9, "nombre": "Algoritmos y estructuras de datos"},
        {"codigo_materia": 10, "nombre": "Teoría de algoritmos"},
        {"codigo_materia": 11, "nombre": "Modelación numérica"},
        {"codigo_materia": 12, "nombre": "Ingeniería de software"},
        {"codigo_materia": 13, "nombre": "Física"},
        {"codigo_materia": 14, "nombre": "Taller de programación"},
        {"codigo_materia": 15, "nombre": "Programación concurrente"},
        {"codigo_materia": 16, "nombre": "Seguridad informática"},
        {"codigo_materia": 17, "nombre": "Gestión del desarrollo de sistemas informáticos"},
        {"codigo_materia": 18, "nombre": "Redes"},
        {"codigo_materia": 19, "nombre": "Sistemas distribuidos"},
        {"codigo_materia": 20, "nombre": "EBT"}
    ]
    return render_template('materias.html', materias=materias)

@app.route("/grupos")
def mostrar_grupos():
    grupos = [
    {'id': 1, 'nombre': 'Nombre de grupo 1', 'materia': 'Fundamentos de la programación'},
    {'id': 2, 'nombre': 'Nombre de grupo 2', 'materia': 'Base de datos'},
    {'id': 3, 'nombre': 'Nombre de grupo 3', 'materia': 'Sistemas operativos'},
    {'id': 4, 'nombre': 'Nombre de grupo 4', 'materia': 'Teoría de algoritmos'},
    {'id': 5, 'nombre': 'Nombre de grupo 5', 'materia': 'Organización del Computador'},
    {'id': 6, 'nombre': 'Nombre de grupo 6', 'materia': 'Programación concurrente'},
    {'id': 7, 'nombre': 'Nombre de grupo 7', 'materia': 'EBT'},
    {'id': 8, 'nombre': 'Nombre de grupo 8', 'materia': 'Paradigmas de programación'},
    {'id': 9, 'nombre': 'Nombre de grupo 9', 'materia': 'Seguridad informática'}
    ]
    return render_template("grupos.html", grupos=grupos)

if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)