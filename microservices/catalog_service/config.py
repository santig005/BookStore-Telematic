import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bookstore_user:bookstore_pass_rds@bookstoredatabase.cbiioglwithm.us-east-1.rds.amazonaws.com/bookstore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'catalog_secret_key' 