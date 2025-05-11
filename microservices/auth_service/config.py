import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://user:12345678@localhost/users_db'  # Replace with your database URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False