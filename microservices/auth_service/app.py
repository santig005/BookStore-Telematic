# auth_service/app.py
from flask import Flask
from flask_login import LoginManager
from .config import Config
from .extensions import db              # <<— your single db instance
from .controller.auth_controller import bp as auth_bp, login_manager as auth_login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # register the one-and-only SQLAlchemy
    db.init_app(app)

    # register your auth blueprint
    app.register_blueprint(auth_bp)

    # init Flask-Login (we’ll reuse the one you defined in auth_controller)
    auth_login_manager.init_app(app)
    auth_login_manager.login_view = 'auth.login'

    # create tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0')
