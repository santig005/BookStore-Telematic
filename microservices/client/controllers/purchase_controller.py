import requests
from flask import Blueprint, request, redirect, url_for, flash, session

purchase = Blueprint('purchase', __name__, url_prefix='/purchase')
PURCHASE_SERVICE_URL = 'http://localhost:5002/purchase'

@purchase.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    # 1) Check your session for the logged-in user
    user_id    = session.get('user_id')
    user_email = session.get('user_email')
    user_name  = session.get('user_name')

    if not user_id:
        flash('Por favor inicia sesión', 'error')
        return redirect(url_for('auth.login'))

    # 2) Read form inputs
    quantity = int(request.form.get('quantity', 1))
    price    = float(request.form.get('price', 0.0))

    # 3) Forward to Purchase service with user info
    try:
        resp = requests.post(
            f"{PURCHASE_SERVICE_URL}/buy/{book_id}",
            json={
                'quantity': quantity,
                'price':    price,
                'user_id':  user_id
            },
            timeout=10
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        flash(f'Error al crear la compra: {e}', 'error')
        return redirect(url_for('catalog.index'))

    data = resp.json()

    # 4) Redirect to payment, include the total
    return redirect(
        url_for('payment.payment_page',
                purchase_id=data['purchase_id'],
                total=data['total_price'])
    )
