from flask import Blueprint, request, jsonify
from app.models.users import User
from app import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users-create', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": {"id": new_user.id}}), 201

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

@users_bp.route('/users-update/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
