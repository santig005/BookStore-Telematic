from flask import Blueprint, jsonify, request
from ..models.book import Book
from ..extensions import db

catalog = Blueprint('catalog', __name__)

@catalog.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    } for book in books])

@catalog.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    })

@catalog.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data['stock'],
        seller_id=data['seller_id']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
        'id': new_book.id,
        'title': new_book.title,
        'author': new_book.author,
        'description': new_book.description,
        'price': new_book.price,
        'stock': new_book.stock,
        'seller_id': new_book.seller_id
    }), 201

@catalog.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.description = data.get('description', book.description)
    book.price = data.get('price', book.price)
    book.stock = data.get('stock', book.stock)
    
    db.session.commit()
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    })

@catalog.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

@catalog.route('/api/books/seller/<int:seller_id>', methods=['GET'])
def get_seller_books(seller_id):
    books = Book.query.filter_by(seller_id=seller_id).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    } for book in books]) 