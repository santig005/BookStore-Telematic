from flask import Flask
from .config     import Config
from .extensions import db

# Import your blueprints by the names you actually defined
from .controller.purchase_controller import purchase as purchase_bp
from .controller.payment_controller  import payment  as payment_bp
from .controller.delivery_controller import delivery as delivery_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Register blueprints—this mounts the URLs
    app.register_blueprint(purchase_bp)  # => /purchase
    app.register_blueprint(payment_bp)   # => /payment
    app.register_blueprint(delivery_bp)  # => /delivery

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    create_app().run(
        debug=True,
        host="0.0.0.0",
        port=5001
    )
