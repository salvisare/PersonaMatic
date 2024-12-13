from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.DevelopmentConfig'):
    """Application factory function."""
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.users import users_bp
    from app.routes.personas import personas_bp
    from app.routes.user_uploaded_data import uploads_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/api/')
    app.register_blueprint(personas_bp, url_prefix='/api/')
    app.register_blueprint(uploads_bp, url_prefix='/api/')

    # Print all registered routes
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint} -> {rule.rule}")

    # Default error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "An internal error occurred"}, 500

    return app
