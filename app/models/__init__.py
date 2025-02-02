import os
import openai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize database and migrations (Only definitions, no Flask app)
db = SQLAlchemy()
migrate = Migrate()

# ✅ Import models so they are accessible
from .users import User
from .personas import PersonasBaseData
from .user_uploaded_data import UserUploadedData

# ✅ Set OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
