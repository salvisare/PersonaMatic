# In app/routes/__init__.py or app.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Welcome to the Flask App!", 200

