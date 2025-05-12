import requests
from flask import Blueprint, request, jsonify, redirect, url_for
from ..extensions import db
from ..models.book import Book
from ..models.purchase import Purchase

purchase = Blueprint('purchase', __name__, url_prefix='/purchase')
AUTH_SERVICE_URL = 'http://127.0.0.1:5000/auth'

def get_current_user():
    cookie = request.cookies.get('session')
    if not cookie:
        return None
    resp = requests.get(f'{AUTH_SERVICE_URL}/whoami',
                        cookies={'session': cookie},
                        timeout=2)
    if resp.status_code != 200:
        return None
    return resp.json()

@purchase.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Login required'}), 401

    # Support both JSON and form posts:
    if request.is_json:
        data      = request.get_json()
        raw_qty   = data.get('quantity')
        raw_price = data.get('price')
    else:
        raw_qty   = request.form.get('quantity')
        raw_price = request.form.get('price')

    # Validate presence
    if raw_qty is None or raw_price is None:
        return jsonify({'error': 'quantity and price are required'}), 400

    # Convert types safely
    try:
        quantity = int(raw_qty)
        price    = float(raw_price)
    except (ValueError, TypeError):
        return jsonify({'error': 'quantity must be integer and price numeric'}), 400

    # ←– New: explicit lookup & not-found handling
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'error': f'Book with id {book_id} not found'}), 404

    if book.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400

    total = price * quantity
    purchase = Purchase(
        user_id     = user['id'],
        book_id     = book_id,
        quantity    = quantity,
        total_price = total,
        status      = 'Pending Payment'
    )

    book.stock -= quantity
    db.session.add(purchase)
    db.session.commit()

    return redirect(url_for('payment.payment_page', purchase_id=purchase.id))