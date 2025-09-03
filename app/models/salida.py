
from app import db

class Salida(db.Model):
    idSalida = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    ingreso_id = db.Column(db.Integer, db.ForeignKey('ingreso.idIngreso'), nullable=False)
    super_id = db.Column(db.Integer, db.ForeignKey('super.idSuper'), nullable=False)  # 👈 falta esta FK

    fecha = db.Column(db.Date, nullable=False)
    hora_salida = db.Column(db.Time, nullable=False)
    horario = db.Column(db.Enum('Mañana', 'Tarde', 'Noche'), nullable=False)

    ingreso = db.relationship('Ingreso', backref=db.backref('salida', uselist=False))
