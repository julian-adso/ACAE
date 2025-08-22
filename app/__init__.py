from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    # Importar Blueprints
    from .routes.user_routes import user_bp

    # Registrar Blueprints
    app.register_blueprint(user_bp)

    return app