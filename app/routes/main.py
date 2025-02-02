from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint, flash, session
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from .users import User
from app.routes.users import create_user

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def home():
    """Handles user registration and ensures unique accounts."""
    message = None

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # ✅ Validate input fields
        if not all([username, email, password, first_name, last_name]):
            message = "All fields are required."
        elif len(password) < 8:
            message = "Password must be at least 8 characters long."
        else:
            # ✅ Check if email or username is already registered
            existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
            if existing_user:
                message = "A user with this email or username already exists. Please log in."
            else:
                try:
                    # ✅ Create new user with hashed password
                    new_user = User(
                        username=username,
                        email=email,
                        password=generate_password_hash(password),  # Hash password
                        first_name=first_name,
                        last_name=last_name
                    )
                    db.session.add(new_user)
                    db.session.commit()

                    # ✅ Store the user ID in session (Ensure correct ID field is used)
                    session["user_id"] = new_user.id  # Use `id`, NOT `user_id`

                    flash("Registration successful!", "success")
                    return redirect(url_for('main.success', username=username))

                except IntegrityError:
                    db.session.rollback()
                    message = "An error occurred. Please try again."

    return render_template("index.html", message=message)


@main_bp.route("/success")
def success():
    username = request.args.get('username', 'Guest')  # Default to 'Guest' if missing
    return render_template("success.html", username=username)


@main_bp.route('/health')
def health_check():
    """Route for checking the health of the application."""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running correctly!'
    }), 200