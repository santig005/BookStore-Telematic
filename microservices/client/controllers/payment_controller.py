import requests
from flask import Blueprint, request, render_template, redirect, url_for, flash, session

payment = Blueprint('payment', __name__, url_prefix='/payment')
API_BASE_URL = 'http://localhost:5002'
PAYMENT_API_URL = f"{API_BASE_URL}/payment"

@payment.route('/<int:purchase_id>', methods=['GET', 'POST'])
def payment_page(purchase_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Por favor inicia sesión', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')
        try:
            resp = requests.post(
                f"{PAYMENT_API_URL}/{purchase_id}",
                json={'method': method, 'amount': amount, 'user_id': user_id},
                timeout=10
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            flash(f'Error al procesar el pago: {e}', 'error')
            return redirect(url_for('payment.payment_page', purchase_id=purchase_id))
        return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))

    total_price = request.args.get('total', '')
    return render_template('payment/payment.html',
                           purchase_id=purchase_id,
                           total_price=total_price)