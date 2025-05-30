from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave-secreta'  # Necesaria para usar sesión

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/usuario")
def usuario():
    return render_template("usuario.html", usuario=usuario)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()  
    return redirect(url_for("index"))  

if __name__ == "__main__":
    app.run("localhost", port=8000, debug=True)
