# purchase_service/app.py

import os
from flask import Flask, render_template
from .config     import Config
from .extensions import db

from .controller.purchase_controller import purchase   as purchase_bp
from .controller.payment_controller  import payment    as payment_bp
from .controller.delivery_controller import delivery   as delivery_bp

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates')
    )
    app.config.from_object(Config)
    db.init_app(app)

    # 1) Home page so url_for('home') resolves:
    @app.route('/', endpoint='home')
    def home():
        # you’ll need a templates/home.html in purchase_service/templates
        return render_template('home.html')

    # 2) register your blueprints as before
    app.register_blueprint(purchase_bp)  
    app.register_blueprint(payment_bp)   
    app.register_blueprint(delivery_bp)  

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    create_app().run(debug=True, port=5001)