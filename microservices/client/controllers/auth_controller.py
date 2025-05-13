import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import os

auth_bp = Blueprint('auth', __name__)

# Configuración de los microservicios
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5001/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            email = request.form.get('email')
            password = request.form.get('password')

            # Llamar al microservicio de autenticación
            response = requests.post(
                f'{AUTH_SERVICE_URL}/login',
                json={
                    'email': email,
                    'password': password
                }
            )

            if response.status_code == 200:
                user_data = response.json()
                print("la user data es:", user_data)
                # Guardar información del usuario en la sesión
                session['user_id'] = user_data.get('id')
                session['user_name'] = user_data.get('user_name')
                session['user_email'] = user_data.get('email')
                flash('Inicio de sesión exitoso', 'success')
                print("los datosss son;", session['user_name'])
                return redirect(url_for('catalog.index'))
            else:
                flash('Credenciales inválidas', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Error al conectar con el servicio de autenticación: {str(e)}', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Validar que las contraseñas coincidan
            if password != confirm_password:
                flash('Las contraseñas no coinciden', 'error')
                return render_template('auth/register.html')

            # Llamar al microservicio de autenticación para el registro
            response = requests.post(
                f'{AUTH_SERVICE_URL}/register',
                json={
                    'name': name,
                    'email': email,
                    'password': password
                }
            )

            if response.status_code == 201:
                flash('Registro exitoso. Por favor, inicia sesión.', 'success')
                return redirect(url_for('auth.login'))
            else:
                error_data = response.json()
                flash(f'Error en el registro: {error_data.get("message", "Error desconocido")}', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Error al conectar con el servicio de autenticación: {str(e)}', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    try:
        # Opcionalmente, notificar al microservicio de autenticación
        if session.get('user_id'):
            requests.post(f'{AUTH_SERVICE_URL}/logout', json={'user_id': session.get('user_id')})
    except requests.exceptions.RequestException:
        # Si hay error al notificar al servicio, continuamos con el logout local
        pass
    
    # Limpiar la sesión
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('catalog.index')) 