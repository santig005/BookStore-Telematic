import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DATABASE_URL')
        or 'mysql+pymysql://bookstore_user:bookstore_pass_rds'
        '@bookstoredatabase.cbiioglwithm.us-east-1.rds.amazonaws.com'
        ':3306/bookstore'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False