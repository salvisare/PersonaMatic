from app import db
from datetime import datetime
from pydantic import BaseModel


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
    # uploaded_files = db.relationship('UserUploadedData', backref='persona', cascade="all, delete-orphan")

    # Relationships for goals, motivations, etc.
    goals = db.relationship('PersonaGoals', backref='persona', cascade="all, delete-orphan")
    motivations = db.relationship('PersonaMotivations', backref='persona', cascade="all, delete-orphan")
    frustrations = db.relationship('PersonaFrustrations', backref='persona', cascade="all, delete-orphan")


class PersonasBaseDataAI(BaseModel):
    name: str
    # additional_title: str
    # description: str
    age: int
    gender: str
    occupation: str
    description: str
    quote_summarized: str
    goals: list[str]
    motivations: list[str]
    frustrations: list[str]
    activities: list[str]


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


class PersonaActivities(db.Model):
    __tablename__ = 'persona_activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)
    activity_01 = db.Column(db.Text, nullable=True)
    activity_02 = db.Column(db.Text, nullable=True)
    activity_03 = db.Column(db.Text, nullable=True)
    activity_04 = db.Column(db.Text, nullable=True)
    activity_05 = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PersonaDigitalUse(db.Model):
    __tablename__ = 'persona_digital_use'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)
    desktop_use = db.Column(db.Boolean, nullable=False, default=False)  # True/False for use
    mobile_use = db.Column(db.Boolean, nullable=False, default=False)
    social_media_use = db.Column(db.Boolean, nullable=False, default=False)
    computer_literacy = db.Column(db.Boolean, nullable=False, default=False)
    frequently_used_tools_and_apps = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PersonaQuotes(db.Model):
    __tablename__ = 'persona_quotes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas_base_data.id'), nullable=False)
    quote_01 = db.Column(db.Text, nullable=True)
    quote_02 = db.Column(db.Text, nullable=True)
    quote_03 = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
