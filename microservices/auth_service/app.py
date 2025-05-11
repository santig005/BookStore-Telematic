from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from controllers import auth_controller
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)  # Load database configuration
db = SQLAlchemy(app)

#Import models
from models import models

app.register_blueprint(auth_controller.bp)

#Flask login config
login_manager = LoginManager()
login_manager.init_app(app) #This line is necessary
login_manager.login_view = 'auth.login'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')