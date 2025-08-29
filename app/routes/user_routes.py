
from flask import Blueprint, render_template, request, jsonify,redirect, url_for, flash, session, jsonify
from app.models.decorators import login_required
from app.models.ingreso import Ingreso
from ..models.salida import Salida
from .. import db
from app.models.user import User
from app.models.admin import Admin
from app.models.login import Login
from datetime import date, datetime
import hashlib
<<<<<<< HEAD
from app import db
from flask import session, render_template

=======
from collections import defaultdict
>>>>>>> b4a095288f0fdb0ed959856b319d410c1b33d3ae

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
                    session['username'] = user.usernameUser   # Guardamos el nombre real del usuario
                    session['role'] = 'user'
                    return redirect(url_for('user.index'))  # Página de usuarios (index.html)

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

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@user_bp.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    usuario = User.query.get(session['user_id'])

    hoy = datetime.now()

    # Contar asistencias y ausencias del mes actual
    # CORRECCIÓN: Cambiar 'usuario_id' por 'user_id'
    asistencias = Ingreso.query.filter_by(user_id=usuario.idUser, estado='Asistencia')\
                               .filter(db.extract('month', Ingreso.fecha) == hoy.month).count()

    # CORRECCIÓN: Cambiar 'usuario_id' por 'user_id'
    ausencias = Ingreso.query.filter_by(user_id=usuario.idUser, estado='Ausencia')\
                             .filter(db.extract('month', Ingreso.fecha) == hoy.month).count()

    # Historial últimos 10 ingresos
    # CORRECCIÓN: Cambiar 'usuario_id' por 'user_id'
    historial = Ingreso.query.filter_by(user_id=usuario.idUser)\
                             .order_by(Ingreso.fecha.desc(), Ingreso.hora.desc())\
                             .limit(10).all()

    return render_template(
        'index.html',
        username=usuario.usernameUser,
        asistencias=asistencias,
        ausencias=ausencias,
        historial=historial
    )
@user_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('user.login'))

    # Aquí puedes traer estadísticas generales, lista de usuarios, etc.
    return render_template('dashboard.html', username=session['username'])

# Registrar el horario y el ingreso
def determinar_horario_actual():
    ahora = datetime.now().time()

    if ahora >= datetime.strptime("06:00", "%H:%M").time() and ahora < datetime.strptime("12:00", "%H:%M").time():
        return "Mañana"
    elif ahora >= datetime.strptime("12:00", "%H:%M").time() and ahora < datetime.strptime("18:00", "%H:%M").time():
        return "Tarde"
    else:
        return "Noche"


@user_bp.route('/registrar_ingreso', methods=['POST'])
def registrar_ingreso():
    data = request.get_json()
    documento = data.get('documento')
    motivo = data.get('motivo')  # puede venir vacío o no

    if not documento:
        return jsonify({'success': False, 'message': 'Documento requerido'}), 400

    usuario = User.query.filter_by(documentUser=documento).first()
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    # Horario actual y horario esperado
    horario_actual = determinar_horario_actual()
    horario_trabajador = usuario.horario  # ⚠️ Asegúrate de que User tenga este campo

    # Si ya tiene ingreso registrado hoy
    ingreso = Ingreso.query.filter_by(user_id=usuario.idUser, fecha=date.today()).order_by(Ingreso.idIngreso.desc()).first()

    if ingreso:
        salida = Salida.query.filter_by(ingreso_id=ingreso.idIngreso).first()
        if salida:
            # Permitir nuevo ingreso solo con motivo
            if not motivo:
                return jsonify({
                    'success': False,
                    'message': 'Debe ingresar un motivo para volver a entrar.'
                }), 400

            nuevo_ingreso = Ingreso(
                user_id=usuario.idUser,
                fecha=date.today(),
                hora=datetime.now().time(),
                horario=horario_actual,
                estado='Presente',
                motivo=motivo
            )
            db.session.add(nuevo_ingreso)
            db.session.commit()

            return jsonify({'success': True, 'message': f'Nuevo ingreso registrado con motivo: {motivo}'})

        else:
            # Registrar salida
            nueva_salida = Salida(
                user_id=usuario.idUser,
                ingreso_id=ingreso.idIngreso,
                fecha=date.today(),
                hora_salida=datetime.now().time(),
                horario=ingreso.horario
            )
            db.session.add(nueva_salida)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Salida registrada'})

    else:
        # Primer ingreso del día
        if horario_actual != horario_trabajador and not motivo:
            return jsonify({
                'success': False,
                'message': f'El horario actual es {horario_actual}, pero su horario asignado es {horario_trabajador}. Ingrese un motivo para continuar.'
            }), 400

        nuevo_ingreso = Ingreso(
            user_id=usuario.idUser,
            fecha=date.today(),
            hora=datetime.now().time(),
            horario=horario_actual,
            estado='Presente',
            motivo=motivo
        )
        db.session.add(nuevo_ingreso)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Ingreso registrado'})

@user_bp.route('/api/empleados')
def obtener_empleados():
    usuarios = User.query.all()
    empleados = [
        {
            'id': u.idUser,
            'name': u.usernameUser   # 👈 asegúrate de que tu modelo User tenga este campo
        }
        for u in usuarios
    ]
    return jsonify(empleados)

@user_bp.route('/api/empleado/<int:user_id>/asistencia')
def obtener_asistencia(user_id):
    usuario = User.query.get(user_id)
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    ingresos = Ingreso.query.filter_by(user_id=user_id).all()
    eventos = []

    for ingreso in ingresos:
        # Evento de ingreso
        eventos.append({
            'title': f'Ingreso: {ingreso.hora.strftime("%H:%M")}',
            'start': f"{ingreso.fecha.strftime('%Y-%m-%d')}T{ingreso.hora.strftime('%H:%M:%S')}",
            'className': 'ingreso',
            'tipo': 'ingreso',
            'extendedProps': {
                'fecha': ingreso.fecha.strftime("%Y-%m-%d"),
                'hora': ingreso.hora.strftime("%H:%M"),
                'estado': ingreso.estado,
                'motivo': ingreso.motivo,
                'horario': ingreso.horario
            }
        })

        # Evento de salida (si existe)
        if ingreso.salida:
            salida = ingreso.salida
            eventos.append({
                'title': f'Salida: {salida.hora_salida.strftime("%H:%M")}',
                'start': f"{salida.fecha.strftime('%Y-%m-%d')}T{salida.hora_salida.strftime('%H:%M:%S')}",
                'className': 'salida',
                'tipo': 'salida',
                'extendedProps': {
                    'fecha': salida.fecha.strftime("%Y-%m-%d"),
                    'hora': salida.hora_salida.strftime("%H:%M"),
                    'horario': salida.horario
                }
            })

    return jsonify({'success': True, 'eventos': eventos})

