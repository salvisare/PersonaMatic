from flask import Blueprint, request, jsonify, session, url_for, current_app
from werkzeug.security import check_password_hash
from app.models.users import User
from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import logging

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def create_user(username, email, password, first_name, last_name):
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user": {"id": new_user.id}}), 201
    except IntegrityError as e:
        # Handle email already exists or other unique constraint errors
        return jsonify({"message": "Email already exists or invalid data provided."}), 400  # Bad request
    except Exception as e:
        # Handle unexpected errors
        return jsonify(
            {"message": "An unexpected error occurred. Please try again later."}), 500  # Internal server error


@users_bp.route('/users-retrieve', methods=['GET'])
def retrieve_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

@users_bp.route('/users-retrieve/<int:id>', methods=['GET'])
def retrieve_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    })

@users_bp.route('/users-update/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@users_bp.route('/users-delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id  # ✅ Ensure session is set
    session.modified = True  # ✅ Ensure session is saved
    print("Session set for user:", session.get("user_id"))  # ✅ Debugging Step

    return jsonify({"message": "Login successful", "redirect_url": url_for("uploads.uploads_list")})