from app import db

class Login(db.Model):
    __tablename__ = 'login'
    idLogin = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usernameLogin = db.Column(db.String(50), unique=True, nullable=False)
    passwordLogin = db.Column(db.String(100), nullable=False)
    roleLogin = db.Column(db.enum('admin','user'), nullable=False)