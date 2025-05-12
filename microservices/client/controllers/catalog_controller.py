import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

catalog_bp = Blueprint('catalog', __name__)

# Configuración de los microservicios
CATALOG_SERVICE_URL = os.getenv('CATALOG_SERVICE_URL', 'http://localhost:5003/api/')
CART_SERVICE_URL = os.getenv('CART_SERVICE_URL', 'http://localhost:5002')

@catalog_bp.route('/')
def index():
    try:
        # Obtener libros del servicio de catálogo
        response = requests.get(f'{CATALOG_SERVICE_URL}/books')
        if response.status_code == 200:
            books = response.json()
            return render_template('catalog/index.html', books=books)
        else:
            flash('Error al obtener el catálogo de libros', 'error')
            return render_template('catalog/index.html', books=[])
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con el servicio de catálogo: {str(e)}', 'error')
        return render_template('catalog/index.html', books=[])

@catalog_bp.route('/add-to-cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    try:
        quantity = int(request.form.get('quantity', 1))
        # Agregar libro al carrito con la cantidad especificada
        response = requests.post(
            f'{CART_SERVICE_URL}/cart/add/{book_id}',
            json={'quantity': quantity}
        )
        if response.status_code == 200:
            flash('Libro agregado al carrito', 'success')
        else:
            flash('Error al agregar libro al carrito', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con el servicio de carrito: {str(e)}', 'error')
    return redirect(url_for('catalog.index')) 