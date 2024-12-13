from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import models to make them accessible
from .users import User
from .personas import PersonasBaseData
from .user_uploaded_data import UserUploadedData

# Initialize the SQLAlchemy and Migrate instances
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Set up your database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/db/app.db'  # Adjust the path as needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints or routes
    from app.routes.main import main_bp
    from app.routes.users import users_bp
    from app.routes.personas import personas_bp
    from app.routes.user_uploaded_data import uploads_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(personas_bp)
    app.register_blueprint(uploads_bp)

    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Route: {rule}")

    return app

