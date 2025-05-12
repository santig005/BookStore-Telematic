import requests
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    current_app,
    jsonify
)
from ..extensions import db
from ..models.delivery import DeliveryProvider
from ..models.delivery_assignment import DeliveryAssignment

delivery = Blueprint('delivery', __name__, url_prefix='/delivery')
AUTH_SERVICE_URL = 'http://127.0.0.1:5000/auth'

def get_current_user():
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        return None

    resp = requests.get(
        f'{AUTH_SERVICE_URL}/whoami',
        cookies={'session': session_cookie},
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
        raw = request.form.get('provider')
        try:
            provider_id = int(raw)
        except (TypeError, ValueError):
            return jsonify({'error':'provider id must be an integer'}), 400

        assignment = DeliveryAssignment(
            purchase_id = purchase_id,
            provider_id = provider_id
        )
        db.session.add(assignment)
        db.session.commit()

        # ←— build external Catalog URL and redirect there
        catalog_base = current_app.config['CATALOG_SERVICE_URL']
        # if your Catalog mounts its `catalog()` at GET /book/catalog:
        return redirect(f"{catalog_base}/book/catalog")

    # GET: show options
    return render_template(
        'delivery_options.html',
        providers=providers,
        purchase_id=purchase_id
    )
