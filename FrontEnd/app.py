import sys
import os

# Agrega la carpeta raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))





# app.py
from flask import Flask, render_template, session, redirect, url_for, request
from BackEnd.routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth/registrarse")



@app.route('/')
def home():
    usuario = session.get('padron')
    return render_template('index.html', usuario=usuario)










'''

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

'''





























@app.route("/perfil_de_usuario")
def perfil_de_usuario():
    return f"Bienvenido al perfil de {session['usuario']}"  # muestra el perfil del usuario a través del botón "Mi perfil"

grupos = [
    {'id': 1, 'nombre': 'Nombre de grupo 1', 'codigo_materia': 1},
    {'id': 2, 'nombre': 'Nombre de grupo 2', 'codigo_materia': 1},
    {'id': 3, 'nombre': 'Nombre de grupo 3', 'codigo_materia': 1},
    {'id': 4, 'nombre': 'Nombre de grupo 4', 'codigo_materia': 1},
    {'id': 5, 'nombre': 'Nombre de grupo 5', 'codigo_materia': 1},
    {'id': 6, 'nombre': 'Nombre de grupo 6', 'codigo_materia': 1},
    {'id': 7, 'nombre': 'Nombre de grupo 7', 'codigo_materia': 1},
    {'id': 8, 'nombre': 'Nombre de grupo 8', 'codigo_materia': 1},
    {'id': 9, 'nombre': 'Nombre de grupo 9', 'codigo_materia': 1}
]

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

@app.route("/grupos")
def mostrar_grupos():
    return render_template("grupos.html", grupos=grupos)

@app.route("/materias")
def mostrar_materias():
    return render_template('materias.html', materias=materias)

@app.route("/materia/<int:codigo_materia>")
def grupos_por_materia(codigo_materia):
    # Buscar la materia seleccionada
    for m in materias:
        if m["codigo_materia"] == codigo_materia:
            materia = m
            break

    grupos_de_materia = [grupo for grupo in grupos if grupo["codigo_materia"] == codigo_materia]

    return render_template("grupos_por_materia.html", materia=materia, grupos=grupos_de_materia)

@app.route("/materias/<int:codigo_materia>/companieros-sin-grupo")
def companieros_sin_grupo_por_materia(codigo_materia):
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


@app.route("/usuario")
def usuario():
    avatares = ["pepe.jpg", "tiger.jpg", "mulan.jpg", "jon.jpg", "lisa.jpg", "snoopy.jpg", "this_is_fine.jpg", "tom.jpg", "coraje.jpg"]
    grupos = [
        {"id": 1, "nombre": "Grupo A", "integrantes": 5},
        {"id": 2, "nombre": "Grupo B", "integrantes": 3},
        {"id": 3, "nombre": "Grupo C", "integrantes": 6},
    ]

    materias = {
        "cursando": ["Álgebra I", "Análisis II", "Física I"],
        "aprobadas": ["IPC", "Análisis I"],
        "horarios": ["Lunes 18-21", "Miércoles 14-17"]
    }
    
    return render_template("perfil_de_usuario.html", materias=materias, grupos=grupos, avatares=avatares)



if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)