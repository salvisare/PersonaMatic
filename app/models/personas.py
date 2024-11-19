from app import db
from datetime import datetime

class PersonasBaseData(db.Model):
    __tablename__ = 'personas_base_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    additional_title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    quote_summarized = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
