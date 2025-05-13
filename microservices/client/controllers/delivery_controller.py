# microservices/client/controllers/delivery_controller.py

import requests
from flask import Blueprint, request, render_template, redirect, url_for, flash, session

delivery = Blueprint('delivery', __name__, url_prefix='/delivery')

API_BASE_URL     = 'http://localhost:5002'
DELIVERY_API_URL = f"{API_BASE_URL}/delivery"

@delivery.route('/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    # 1) Ensure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('Por favor inicia sesión', 'error')
        return redirect(url_for('auth.login'))

    # 2) Handle form submission
    if request.method == 'POST':
        provider_id = request.form.get('provider')
        try:
            resp = requests.post(
                f"{DELIVERY_API_URL}/{purchase_id}",
                json={'provider': provider_id, 'user_id': user_id},
                timeout=5
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            flash(f'Error al programar la entrega: {e}', 'error')
            return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))

        flash('Entrega programada con éxito', 'success')
        return redirect(url_for('catalog.index'))

    # 3) On GET, fetch available providers from Purchase-Service
    try:
        resp = requests.get(f"{DELIVERY_API_URL}/{purchase_id}", timeout=5)
        resp.raise_for_status()
        providers = resp.json().get('providers', [])
    except requests.RequestException as e:
        flash(f'Error al obtener proveedores: {e}', 'error')
        return redirect(url_for('catalog.index'))

    # 4) Render the delivery selection template
    return render_template(
        'delivery/delivery.html',
        purchase_id=purchase_id,
        providers=providers
    )
