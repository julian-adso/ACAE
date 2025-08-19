from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar Blueprints
    from .routes.user_routes import user_bp
    from .routes.admin_routes import admin_bp

    # Registrar Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    return app
