from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.routes.users import create_user

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def home():
    """Default route for the home page."""
    """
    return jsonify({
        'message': 'Welcome to the PersonaMatic API!',
        'status': 'success'  # Ensure the status key is included here
    }), 200  # Status code 200 indicates success
    """
    #data = {"message": "Welcome to the PersonaMatic API!", "status": "success"}
    #return render_template("index.html", data=data)  # Pass data to the template

    message = None
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # Validation (important!)
        if not username:
            message = "Username is required."
        elif not email:
            message = "Email is required."
        elif not password:
            message = "Password is required."
        elif len(password) < 8:  # Example of password validation
            message = "Password must be at least 8 characters."
        # Add more validation as needed (e.g., email format)
        else:
            response = create_user(username, email, password, first_name, last_name)  # Call create_user
            if response[1] == 201:  # Check status code
                return redirect(url_for('success', username=username))
            else:
                message = response[0].get_json().get('message')  # Get error message from JSON

    return render_template("index.html", message=message)


@main_bp.route("/success/<username>")
def success(username):
    return render_template("success.html", username=username)


@main_bp.route('/health')
def health_check():
    """Route for checking the health of the application."""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running correctly!'
    }), 200