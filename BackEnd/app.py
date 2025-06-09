from flask import Flask
from flask_cors import CORS
from routes.registrar_iniciar_sesion import registrar_iniciar_sesion_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(registrar_iniciar_sesion_bp)

if __name__ == "__main__":
    app.run(debug=True)