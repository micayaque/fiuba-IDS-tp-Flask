from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index ():
    return render_template('index.html')

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
    return render_template("materias.html", materias=materias)

if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)