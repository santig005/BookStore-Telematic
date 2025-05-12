from flask import Flask
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.auth_controller import auth_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Cambia esto por una clave secreta segura

# Registrar los blueprints
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 