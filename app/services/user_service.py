from ..models.user import User
from .. import db

class UserService:
    @staticmethod
    def create_user(data):
        new_user = User(
            name=data['name'],
            email=data['email'],
            role=data['role'],
            password=data['password']  # Make sure to hash the password
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        return user.to_dict() if user else None
