from flask import Blueprint

# Define the blueprint for persona routes
personas_bp = Blueprint('personas', __name__)

@personas_bp.route('/', methods=['GET'])
def get_personas():
    return {"message": "Personas fetched successfully"}