
from flask import Blueprint, render_template, request, jsonify,redirect, url_for, flash, session, jsonify
from app.models.decorators import login_required
from ..models.ingreso import Ingreso
from ..models.salida import Salida
from .. import db
from app.models.user import User
from app.models.admin import Admin
from app.models.login import Login
from datetime import date, datetime
import hashlib

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def home():
    return render_template('home.html')

# Login route
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hashear la contraseña ingresada (SHA1)
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        
        # Buscar en tabla Login
        login = Login.query.filter_by(usernameLogin=username, passwordLogin=hashed_password).first()

        if login:
            # Verificar si corresponde a un User
            user = User.query.filter_by(login_id=login.idLogin).first()
            if user:
                session['user_id'] = user.idUser
                session['username'] = login.usernameLogin
                session['role'] = 'user'
                return redirect(url_for('user.index'))  # Página de usuarios

            # Verificar si corresponde a un Admin
            admin = Admin.query.filter_by(login_id=login.idLogin).first()
            if admin:
                session['admin_id'] = admin.idAdmin
                session['username'] = login.usernameLogin
                session['role'] = 'admin'
                return redirect(url_for('user.dashboard'))  # Página de admins

        # Si no encontró nada
        flash('Usuario o contraseña incorrectos')
        return render_template('login.html')

    return render_template('login.html')

# Logout route
@user_bp.route('/logout')
def logout():
    session.clear()   # Elimina todos los datos de sesión
    return redirect(url_for('user.login'))  # Redirige al login

# Index route
@user_bp.route('/index')
@login_required(role='user')
def index():
    return render_template('index.html')

# Dashboard route
@user_bp.route('/dashboard')
@login_required(role='admin')
def dashboard():
    return render_template('dashboard.html')


@user_bp.route('/registrar_ingreso', methods=['POST'])
def registrar_ingreso():
    data = request.get_json()
    documento = data.get('documento')

    if not documento:
        return jsonify({'success': False, 'message': 'Documento requerido'}), 400

    # Buscar usuario en la tabla User
    usuario = User.query.filter_by(documentUser=documento).first()
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    # Buscar si ya tiene un ingreso registrado HOY
    ingreso = Ingreso.query.filter_by(user_id=usuario.idUser, fecha=date.today()).first()

    if ingreso:
        # Verificar si ya tiene salida asociada
        salida = Salida.query.filter_by(ingreso_id=ingreso.idIngreso).first()
        if salida:
            return jsonify({
                'success': False,
                'message': 'Ya se registró la salida para este usuario hoy'
            }), 400

        # Registrar la salida enlazada al ingreso existente
        nueva_salida = Salida(
            user_id=usuario.idUser,
            ingreso_id=ingreso.idIngreso,
            fecha=date.today(),
            hora_salida=datetime.now().time(),
            horario=ingreso.horario  # mantener el horario del ingreso
        )
        db.session.add(nueva_salida)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Salida registrada'})
    else:
        # Registrar nuevo ingreso si no existe
        nuevo_ingreso = Ingreso(
            user_id=usuario.idUser,
            fecha=date.today(),
            hora=datetime.now().time(),
            horario='Mañana',  # opcional: ajustar dinámicamente
            estado='Presente'
        )
        db.session.add(nuevo_ingreso)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Ingreso registrado'})