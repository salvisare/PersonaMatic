from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Default route for the home page."""
    return jsonify({
        'message': 'Welcome to the PersonaMatic API!',
        'status': 'success'  # Ensure the status key is included here
    }), 200  # Status code 200 indicates success

@main_bp.route('/health')
def health_check():
    """Route for checking the health of the application."""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running correctly!'
    }), 200