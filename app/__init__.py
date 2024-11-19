from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import main_bp  # Import your blueprint

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update to your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.users import users_bp
    from app.routes.personas import personas_bp

    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(personas_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app
