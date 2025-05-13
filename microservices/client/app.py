from flask import Flask
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.auth_controller import auth_bp
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Cambia esto por una clave secreta segura

# Registrar los blueprints
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 