from app import create_app,db
import os

app = create_app()

with app.app_context():
    # Importa los modelos para que SQLAlchemy los registre
    from app.models import admin, user, login, ingreso, historial, salida
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))