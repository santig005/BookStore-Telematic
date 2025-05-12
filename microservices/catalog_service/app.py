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
        
        # Check if we need to add some initial data
        from models.book import Book
        if Book.query.count() == 0:
            # Add some sample books
            sample_books = [
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                    description="A story of the fabulously wealthy Jay Gatsby",
                    price=19.99,
                    stock=10,
                    seller_id=1
                ),
                Book(
                    title="To Kill a Mockingbird",
                    author="Harper Lee",
                    description="The story of racial injustice and the loss of innocence",
                    price=15.99,
                    stock=8,
                    seller_id=1
                )
            ]
            db.session.bulk_save_objects(sample_books)
            db.session.commit()

if __name__ == '__main__':
    app = create_app()
    init_db(app)
    app.run(host='0.0.0.0', port=5002, debug=True) 