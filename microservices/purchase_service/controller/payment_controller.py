# microservices/purchase_service/controller/payment_controller.py

from flask import Blueprint, request, jsonify
from extensions import db
from models.payment import Payment
from models.purchase import Purchase

payment = Blueprint('payment', __name__, url_prefix='/payment')

@payment.route('/<int:purchase_id>', methods=['POST'])
def pay(purchase_id):
    # 1) Parse JSON payload
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 401

    method = data.get('method')
    amount = data.get('amount')
    if method is None or amount is None:
        return jsonify({'error': 'method and amount required'}), 400

    # 2) Load purchase and verify (optional) it belongs to user_id
    purchase = Purchase.query.get_or_404(purchase_id)
    if purchase.user_id != int(user_id):
        return jsonify({'error': 'Unauthorized purchase'}), 403

    # 3) Create Payment record and update Purchase
    pay = Payment(
        purchase_id=purchase_id,
        amount=amount,
        payment_method=method,
        payment_status='Paid'
    )
    purchase.status = 'Paid'

    db.session.add(pay)
    db.session.commit()

    # 4) Return success
    return jsonify({
        'message': 'Payment recorded',
        'purchase_id': purchase_id
    }), 200
