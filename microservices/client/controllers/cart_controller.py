import requests
from flask import Blueprint, render_template, redirect, url_for, flash
import os

cart_bp = Blueprint('cart', __name__)

# Configuración de los microservicios
CART_SERVICE_URL = os.getenv('CART_SERVICE_URL', 'http://localhost:5002')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5003')

@cart_bp.route('/cart')
def view_cart():
    try:
        # Obtener carrito del servicio de carrito
        response = requests.get(f'{CART_SERVICE_URL}/cart')
        cart = response.json() if response.status_code == 200 else {'items': []}
        return render_template('cart/index.html', cart=cart)
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con el servicio de carrito: {str(e)}', 'error')
        return render_template('cart/index.html', cart={'items': []})

@cart_bp.route('/cart/remove/<int:book_id>', methods=['POST'])
def remove_from_cart(book_id):
    try:
        # Remover libro del carrito
        response = requests.delete(f'{CART_SERVICE_URL}/cart/remove/{book_id}')
        if response.status_code == 200:
            flash('Libro removido del carrito', 'success')
        else:
            flash('Error al remover libro del carrito', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con el servicio de carrito: {str(e)}', 'error')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['POST'])
def checkout():
    try:
        # Crear orden
        response = requests.post(f'{ORDER_SERVICE_URL}/orders')
        if response.status_code == 200:
            flash('Orden creada exitosamente', 'success')
            # Limpiar carrito después de crear la orden
            requests.delete(f'{CART_SERVICE_URL}/cart/clear')
        else:
            flash('Error al crear la orden', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con el servicio de órdenes: {str(e)}', 'error')
    return redirect(url_for('catalog.index')) 