
from app import db

class Salida(db.Model):
    
    idSalida = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    ingreso_id = db.Column(db.Integer, db.ForeignKey('ingreso.idIngreso'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)         # Día
    hora_salida = db.Column(db.Time, nullable=False)          # Hora exacta
    horario = db.Column(db.Enum('Mañana', 'Tarde', 'Noche'), nullable=False) # Ejemplo: "Mañana", "Tarde", "Noche"

    ingreso = db.relationship('Ingreso', backref=db.backref('salida', uselist=False))
    