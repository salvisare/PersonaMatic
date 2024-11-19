# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance
db = SQLAlchemy()

# Import models to make them accessible
from .users import User
from .personas import PersonasBaseData
from .user_uploaded_data import UserUploadedData
