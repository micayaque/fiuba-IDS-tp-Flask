from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)

app.secret_key = 'clave-secreta'  # necesaria para usar session

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
    session.pop("usuario", None)                      # para cerrar la sesión, eliminamos al usuario de session
    return redirect(url_for("inicio"))                # volvemos a la página principal

@app.route("/perfil_de_usuario")
def perfil_de_usuario():
    return f"Bienvenido al perfil de {session['usuario']}"  # muestra el perfil del usuario a través del botón "Mi perfil"

@app.route("/materias")
def mostrar_materias():
    return render_template("materias.html", materias=materias)

grupos = [
    {"nombre": "Grupo 1", "codigo_materia": 2, "integrantes": 4},
    {"nombre": "Grupo 2", "codigo_materia": 2, "integrantes": 3},
    {"nombre": "Grupo 3", "codigo_materia": 2, "integrantes": 5},
]

@app.route("/materias/<int:codigo_materia>")
def ver_grupos_por_materia(codigo_materia):
    materia = None
    for m in materias:
       if m["codigo_materia"] == codigo_materia:
            materia = m
            break
    grupos_materia = [grupo for grupo in grupos if grupo["codigo_materia"] == codigo_materia]
    return render_template("grupos_por_materia.html", materia=materia, grupos=grupos_materia)

@app.route("/materias/<int:codigo_materia>/sin-grupo")
def ver_sin_grupo(codigo_materia):
    materia = None
    for m in materias:
        if m["codigo_materia"] == codigo_materia:
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