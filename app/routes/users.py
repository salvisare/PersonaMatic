from flask import Blueprint, request, jsonify
from ..services.user_service import UserService

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    user = UserService.create_user(data)
    return jsonify(user), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/', methods=['GET'])
def get_all_users():
    return {"message": "All users retrieved successfully"}
