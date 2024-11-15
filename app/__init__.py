from flask import Flask
from .config import Config
from .models import db
from .users import users_bp
from .personas import personas_bp

# Explicitly define what is exposed by this package
__all__ = ['users_bp', 'personas_bp']

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app
