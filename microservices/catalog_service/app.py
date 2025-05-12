from flask import Flask
from flask_cors import CORS
from extensions import db
from config import Config
from controller.catalog_controller import catalog

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(catalog)
    
    return app

def init_db(app):
    with app.app_context():
        # Create all tables
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    init_db(app)
    app.run(host='0.0.0.0', port=5002, debug=True) 