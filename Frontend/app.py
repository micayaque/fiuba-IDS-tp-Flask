from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)

app.secret_key = 'clave-secreta'  # necesaria para usar session

@app.route("/usuario")
def usuario():
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
    
    return render_template("perfil_de_usuario.html", materias=materias, grupos=grupos)


@app.route('/logout', methods=['POST'])
def logout():
    # Lógica para cerrar sesión (por ejemplo, eliminar sesión, redirigir, etc.)
    session.clear()
    return redirect(url_for('/'))  # o la ruta que quieras


if __name__ == "__main__":
    app.run("localhost", port=8000, debug=True)
