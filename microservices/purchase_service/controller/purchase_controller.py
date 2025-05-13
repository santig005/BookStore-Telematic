from flask import Blueprint, request, jsonify
from models.purchase import Purchase
from models.book import Book
from extensions import db

purchase = Blueprint('purchase', __name__, url_prefix='/purchase')

@purchase.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    # 1) Parse JSON payload
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 401

    # 2) Extract quantity & price
    try:
        quantity = int(data.get('quantity', 1))
        price    = float(data.get('price', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity or price'}), 400

    # 3) Load book and check stock
    book = Book.query.get_or_404(book_id)
    if book.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400

    # 4) Create Purchase and decrement stock
    total_price = price * quantity
    new_purchase = Purchase(
        user_id=user_id,
        book_id=book_id,
        quantity=quantity,
        total_price=total_price,
        status='Pending Payment'
    )
    book.stock -= quantity
    db.session.add(new_purchase)
    db.session.commit()

    # 5) Return JSON for client to continue flow
    return jsonify({
        'purchase_id': new_purchase.id,
        'total_price': total_price
    }), 201
