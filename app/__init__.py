import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()

# ✅ Retrieve API Key and Secret Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")


def create_app(config_class='config.DevelopmentConfig'):
    """Flask application factory function."""
    app = Flask(__name__)

    # ✅ Load configuration
    app.config.from_object(config_class)
    app.config["SECRET_KEY"] = SECRET_KEY  # Load SECRET_KEY securely

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Register Blueprints (Routes)
    from app.routes.main import main_bp
    from app.routes.users import users_bp
    from app.routes.personas import personas_bp
    from app.routes.user_uploaded_data import uploads_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/api/')
    app.register_blueprint(personas_bp, url_prefix='/api/')
    app.register_blueprint(uploads_bp, url_prefix='/api/')

    # ✅ Debugging: Print all registered routes
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint} -> {rule.rule}")

    # ✅ Default error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "An internal error occurred"}, 500

    return app
