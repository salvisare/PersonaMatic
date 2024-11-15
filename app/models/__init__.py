# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance
db = SQLAlchemy()

# Import models to make them accessible
from .user import User
from .persona import Persona
