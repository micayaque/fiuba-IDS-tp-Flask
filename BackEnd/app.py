from flask import Flask
from flask_cors import CORS
from routes.registrar_iniciar_sesion import registrar_iniciar_sesion_bp
from routes.materias import materias_bp
from routes.grupos import grupos_bp
from routes.perfil_usuario import perfil_usuario_bp
from routes.solicitudes import solicitudes_bp
from routes.errores import error_bp

from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

app.register_blueprint(error_bp)
app.register_blueprint(registrar_iniciar_sesion_bp)
app.register_blueprint(materias_bp)
app.register_blueprint(grupos_bp)
app.register_blueprint(perfil_usuario_bp)
app.register_blueprint(solicitudes_bp)

if __name__ == "__main__":
    app.run(debug=True)