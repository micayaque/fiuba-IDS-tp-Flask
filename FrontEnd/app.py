from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index ():
    return render_template('index.html')

@app.route("/materias")
def mostrar_materias():
    materias = [
        {"id": 1, "nombre": "Fundamentos de la programación"},
        {"id": 2, "nombre": "Introducción al desarrollo de software"},
        {"id": 3, "nombre": "Organización del computador"},
        {"id": 4, "nombre": "Probabilidad y estadística"},
        {"id": 5, "nombre": "Sistemas operativos"},
        {"id": 6, "nombre": "Paradigmas de programación"},
        {"id": 7, "nombre": "Base de datos"},
        {"id": 8, "nombre": "Ciencia de datos"},
        {"id": 9, "nombre": "Algoritmos y estructuras de datos"},
        {"id": 10, "nombre": "Teoría de algoritmos"},
        {"id": 11, "nombre": "Modelación numérica"},
        {"id": 12, "nombre": "Ingeniería de software"},
        {"id": 13, "nombre": "Física"},
        {"id": 14, "nombre": "Taller de programación"},
        {"id": 15, "nombre": "Programación concurrente"},
        {"id": 16, "nombre": "Seguridad informática"},
        {"id": 17, "nombre": "Gestión del desarrollo de sistemas informáticos"},
        {"id": 18, "nombre": "Redes"},
        {"id": 19, "nombre": "Sistemas distribuidos"},
        {"id": 20, "nombre": "EBT"}
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