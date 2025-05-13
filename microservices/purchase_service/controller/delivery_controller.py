# microservices/purchase_service/controller/delivery_controller.py

from flask import Blueprint, request, jsonify
from extensions import db
from models.delivery import DeliveryProvider
from models.delivery_assignment import DeliveryAssignment

delivery = Blueprint('delivery', __name__, url_prefix='/delivery')

@delivery.route('/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    # -- GET: return list of providers --
    if request.method == 'GET':
        providers = DeliveryProvider.query.all()
        return jsonify({
            'providers': [
                {
                  'id': p.id,
                  'name': p.name,
                  'coverage_area': p.coverage_area,
                  'cost': p.cost
                } for p in providers
            ]
        }), 200

    # -- POST: assign a provider --
    data = request.get_json() or {}
    user_id = data.get('user_id')
    provider_id = data.get('provider')
    if not user_id or not provider_id:
        return jsonify({'error': 'user_id and provider required'}), 400

    assignment = DeliveryAssignment(
        purchase_id=purchase_id,
        provider_id=provider_id
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'message': 'Delivery scheduled'}), 201
