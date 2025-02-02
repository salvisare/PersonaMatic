from sqlalchemy import ForeignKey, Integer, String, Text, Boolean, DateTime, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db


class UserUploadedData(db.Model):
    __tablename__ = 'user_uploaded_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Removed explicit constraint name
    persona_id = Column(Integer, ForeignKey('personas_base_data.id'), nullable=True)  # Removed explicit constraint name

    file_name = Column(String(255), nullable=True)
    file_path = Column(Text, nullable=True)
    file_type = Column(String(50), nullable=True)
    content = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ Relationship to PersonasBaseData (One-to-One)
    persona = relationship('PersonasBaseData', backref='uploaded_file', uselist=False)
