from flask import Blueprint, request, jsonify
from app.models.personas import PersonasBaseData
from app import db

personas_bp = Blueprint('personas', __name__)

@personas_bp.route('/personas-create', methods=['POST'])
def create_persona():
    data = request.json
    new_persona = PersonasBaseData(
        user_id=data['user_id'],
        photo=data['photo'],
        name=data['name'],
        additional_title=data['additional_title'],
        description=data.get('description'),
        age=data.get('age'),
        gender=data.get('gender'),
        occupation=data.get('occupation'),
        quote_summarized=data['quote_summarized']
    )
    db.session.add(new_persona)
    db.session.commit()
    return jsonify({"message": "Persona created successfully", "persona": {"id": new_persona.id}}), 201

@personas_bp.route('/personas-retrieve', methods=['GET'])
def retrieve_personas():
    personas = PersonasBaseData.query.all()
    return jsonify([{
        "id": persona.id,
        "name": persona.name,
        "photo": persona.photo,
        "user_id": persona.user_id
    } for persona in personas])

@personas_bp.route('/personas-retrieve/<int:id>', methods=['GET'])
def retrieve_persona(id):
    persona = PersonasBaseData.query.get_or_404(id)
    return jsonify({
        "id": persona.id,
        "name": persona.name,
        "photo": persona.photo,
        "user_id": persona.user_id,
        "description": persona.description,
        "age": persona.age,
        "gender": persona.gender,
        "occupation": persona.occupation,
        "quote_summarized": persona.quote_summarized
    })

@personas_bp.route('/personas-update/<int:id>', methods=['PUT'])
def update_persona(id):
    persona = PersonasBaseData.query.get_or_404(id)
    data = request.json
    persona.photo = data.get('photo', persona.photo)
    persona.name = data.get('name', persona.name)
    persona.additional_title = data.get('additional_title', persona.additional_title)
    persona.description = data.get('description', persona.description)
    persona.age = data.get('age', persona.age)
    persona.gender = data.get('gender', persona.gender)
    persona.occupation = data.get('occupation', persona.occupation)
    persona.quote_summarized = data.get('quote_summarized', persona.quote_summarized)
    db.session.commit()
    return jsonify({"message": "Persona updated successfully"})

@personas_bp.route('/personas-update/<int:id>', methods=['DELETE'])
def delete_persona(id):
    persona = PersonasBaseData.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return jsonify({"message": "Persona deleted successfully"})
