from app import db
from datetime import datetime

class UserUploadedData(db.Model):
    __tablename__ = 'user_uploaded_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)  # Add this line
    file_name = db.Column(db.String(255), nullable=True)  # Allow null if you want it optional
    file_path = db.Column(db.Text, nullable=True)
    file_type = db.Column(db.String(50), nullable=True)
    content = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

