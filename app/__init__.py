from flask import Flask
from app.utilidad.extensions import db
from app.routes.user_routes import registrar_ausencias_global

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Importar Blueprints aquí después de inicializar db
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    with app.app_context():
        registrar_ausencias_global()

    return app
