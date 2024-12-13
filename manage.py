from app import create_app, db
from flask_migrate import Migrate
from app.models.users import User
from app.models.personas import PersonasBaseData
from app.models.user_uploaded_data import UserUploadedData

# Initialize app and migrations
app = create_app()
migrate = Migrate(app, db)

# Add migration commands if needed
@app.cli.command('db_init')
def db_init():
    """Initialize the database."""
    db.create_all()
    print("Database initialized.")

@app.cli.command('db_migrate')
def db_migrate():
    """Run database migrations."""
    with app.app_context():
        migrate.init_app(app, db)
        print("Running database migrations...")
        migrate()

@app.cli.command('db_upgrade')
def db_upgrade():
    """Upgrade the database to the latest migration."""
    with app.app_context():
        upgrade()
        print("Database upgraded.")

if __name__ == "__main__":
    app.run(debug=True)
