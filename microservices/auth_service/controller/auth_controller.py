from flask import Blueprint, request, jsonify
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
    LoginManager
)
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'message': 'Name, email, and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    hashed = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(name=name, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    login_user(user)

    return jsonify({
        'message': 'Logged in successfully',
        'id':    user.id,
        'email': user.email,
        'name':  user.name
    }), 200

@bp.route('/whoami', methods=['GET'])
@login_required
def whoami():
    return jsonify({
        'id':    current_user.id,
        'email': current_user.email
    })
