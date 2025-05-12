import requests
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from ..extensions import db
from ..models.delivery import DeliveryProvider
from ..models.delivery_assignment import DeliveryAssignment

delivery = Blueprint('delivery', __name__, url_prefix='/delivery')
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

@delivery.route('/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Login required'}), 401

    providers = DeliveryProvider.query.all()

    if request.method == 'POST':
        provider_id = int(request.form.get('provider'))
        assignment = DeliveryAssignment(
            purchase_id=purchase_id,
            provider_id=provider_id
        )
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('book.catalog'))

    return render_template(
        'delivery_options.html',
        providers=providers,
        purchase_id=purchase_id
    )