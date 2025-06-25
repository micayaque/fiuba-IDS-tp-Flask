from flask import Flask
from flask_cors import CORS

from routes.materias import materias_bp
from routes.grupos import grupos_bp
from routes.usuarios import usuarios_bp
from routes.solicitudes import solicitudes_bp
from routes.sesiones import sesiones_bp

from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

app.register_blueprint(sesiones_bp)
app.register_blueprint(materias_bp)
app.register_blueprint(grupos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(solicitudes_bp)

if __name__ == "__main__":
    app.run(debug=True)