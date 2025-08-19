from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def login():
    return render_template('login.html')

@user_bp.route('/home')
def home():
    return render_template('home.html')
