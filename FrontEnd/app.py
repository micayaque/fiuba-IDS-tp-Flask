from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)

app.secret_key = 'clave-secreta'  # necesaria para usar session

@app.route("/")
def base():
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
    return redirect(url_for("base"))                # volvemos a la página principal

@app.route("/perfil_de_usuario")
def perfil_de_usuario():
    return f"Bienvenido al perfil de {session['usuario']}"  # muestra el perfil del usuario a través del botón "Mi perfil"

if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)