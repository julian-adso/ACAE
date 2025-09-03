from app import create_app, db
import os

# Crear la aplicación con la configuración definida en __init__.py
app = create_app()

# Inicializar la base de datos y registrar los modelos
with app.app_context():
    from app.models import admin, user, login, ingreso, historial, salida, super
    db.create_all()

if __name__ == "__main__":
    # Iniciar el servidor
    app.run(
        debug=True,
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8000))
    )
