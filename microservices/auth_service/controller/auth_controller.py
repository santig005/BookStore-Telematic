from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
import bcrypt
from flask_login import UserMixin, LoginManager

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Configure the login view

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #load the user based in id

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Name, email, and password are required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    login_user(user)  # Use Flask-Login's login_user
    return jsonify({'message': 'Logged in successfully'}), 200


@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()  # Use Flask-Login's logout_user
    return jsonify({'message': 'Logged out successfully'}), 200