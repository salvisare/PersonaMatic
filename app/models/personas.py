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

    # Relationship to uploaded data
    uploaded_files = db.relationship('UserUploadedData', backref='persona', cascade="all, delete-orphan")

    # Relationships for goals, motivations, etc.
    goals = db.relationship('PersonaGoals', backref='persona', cascade="all, delete-orphan")
    motivations = db.relationship('PersonaMotivations', backref='persona', cascade="all, delete-orphan")
    frustrations = db.relationship('PersonaFrustrations', backref='persona', cascade="all, delete-orphan")

class PersonaGoals(db.Model):
    __tablename__ = 'persona_goals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)
    goal_01 = db.Column(db.Text, nullable=False)
    goal_02 = db.Column(db.Text)
    goal_03 = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PersonaMotivations(db.Model):
    __tablename__ = 'persona_motivations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)
    motivation_01 = db.Column(db.Text, nullable=False)
    motivation_02 = db.Column(db.Text)
    motivation_03 = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PersonaFrustrations(db.Model):
    __tablename__ = 'persona_frustrations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)
    frustration_01 = db.Column(db.Text, nullable=False)
    frustration_02 = db.Column(db.Text)
    frustration_03 = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
