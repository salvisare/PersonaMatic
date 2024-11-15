# app/config.py

class Config:
    DEBUG = True
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///your_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
