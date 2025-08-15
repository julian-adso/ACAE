from app import db

class Admin(db.Model):
    idAdmin = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.idLogin'), nullable=False)
    usernameAdmin = db.Column(db.String(50), unique=True, nullable=False)
    passwordAdmin = db.Column(db.String(100), nullable=False)
    documentAdmin = db.Column(db.String(100), nullable=False)
    phoneAdmin = db.Column(db.String(15), nullable=False)
    emailAdmin = db.Column(db.String(100), nullable=False)
    roleAdmin = db.Column(db.Enum('admin', 'user'), nullable=False)
    
    admin = db.relationship('Login', back_populates='admin')
   