import requests
from flask import Blueprint, request, jsonify
from extensions import db
from models.payment import Payment
from models.purchase import Purchase

payment = Blueprint('payment', __name__, url_prefix='/payment')
AUTH_SERVICE_URL = 'http://127.0.0.1:5000/auth'

def get_current_user():
    cookie = request.cookies.get('session')
    if not cookie:
        return None
    resp = requests.get(
        f'{AUTH_SERVICE_URL}/whoami',
        cookies={'session': cookie},
        timeout=2
    )
    if resp.status_code != 200:
        return None
    return resp.json()

@payment.route('/<int:purchase_id>', methods=['GET', 'POST'])
def payment_page(purchase_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Login required'}), 401

    purchase = Purchase.query.get_or_404(purchase_id)

    if request.method == 'POST':
        method = request.form.get('method')
        amount = float(request.form.get('amount'))

        pay = Payment(
            purchase_id=purchase_id,
            amount=amount,
            payment_method=method,
            payment_status='Paid'
        )
        purchase.status = 'Paid'

        db.session.add(pay)
        db.session.commit()
        
        # Devolver una respuesta JSON en lugar de redirigir
        return jsonify({'message': 'Payment successful'}), 200

    # GET: devolver información de pago como JSON
    return jsonify({
        'purchase_id': purchase_id,
        'status': purchase.status
    })
