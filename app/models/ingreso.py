
from app import db

class Ingreso(db.Model):
    
    idIngreso = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)         # Día
    hora = db.Column(db.Time, nullable=False)          # Hora exacta
    horario = db.Column(db.Enum('Mañana', 'Tarde', 'Noche'), nullable=False) # Ejemplo: "Mañana", "Tarde", "Noche"
    estado = db.Column(db.Enum('Presente', 'Retardo', 'Ausente'), nullable=False) # Estado del ingreso
    motivo = db.Column(db.String(255)) # Motivo del ingreso, si aplica

    user = db.relationship('Salida', backref='ingresos')
    