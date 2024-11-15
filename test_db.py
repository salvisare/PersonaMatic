# test_db.py
from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    db.create_all()  # Create tables
    print("Database initialized successfully!")
