import os

basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig:
    # Correct the database URI to match the actual path where app.db is located
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app', 'db', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
