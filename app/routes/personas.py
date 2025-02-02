from flask import Blueprint, request, jsonify, render_template
from app.models.personas import PersonasBaseData, PersonaGoals, PersonaMotivations, PersonaFrustrations
from app.models.user_uploaded_data import UserUploadedData
from app import db

personas_bp = Blueprint('personas', __name__)


@personas_bp.route('/personas-create', methods=['POST'])
def create_persona():
    data = request.json
    try:
        persona = PersonasBaseData(
            user_id=data['user_id'],
            photo=data['photo'],
            name=data['name'],
            additional_title=data['additional_title'],
            description=data.get('description', ''),
            age=data.get('age'),
            gender=data.get('gender', ''),
            occupation=data.get('occupation', ''),
            quote_summarized=data['quote_summarized']
        )
        db.session.add(persona)
        db.session.commit()
        return jsonify({'message': 'Persona created successfully', 'id': persona.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@personas_bp.route('/personas-retrieve', methods=['GET'])
def retrieve_personas():
    personas = PersonasBaseData.query.all()
    results = [
        {
            'id': p.id,
            'name': p.name,
            'additional_title': p.additional_title,
            'description': p.description,
            'age': p.age,
            'gender': p.gender,
            'occupation': p.occupation,
            'quote_summarized': p.quote_summarized
        }
        for p in personas
    ]
    return jsonify(results), 200

@personas_bp.route('/personas-retrieve/<int:id>', methods=['GET'])
def retrieve_persona(id):
    # Retrieve persona by ID
    persona = PersonasBaseData.query.get_or_404(id)

    # Retrieve uploaded files linked to this persona
    uploads = UserUploadedData.query.filter_by(persona_id=persona.id).all()

    # Build the response JSON
    return jsonify({
        'id': persona.id,
        'name': persona.name,
        'additional_title': persona.additional_title,
        'description': persona.description,
        'age': persona.age,
        'gender': persona.gender,
        'occupation': persona.occupation,
        'quote_summarized': persona.quote_summarized,
        'uploaded_files': [
            {
                'file_name': u.file_name,
                'file_path': u.file_path,
                'file_type': u.file_type,
                'content': u.content,
                'uploaded_at': u.uploaded_at,
                'processed': u.processed
            } for u in uploads
        ]
    }), 200

@personas_bp.route('/personas-update/<int:id>', methods=['PUT'])
def update_persona(id):
    data = request.json
    persona = PersonasBaseData.query.get_or_404(id)
    try:
        persona.name = data.get('name', persona.name)
        persona.additional_title = data.get('additional_title', persona.additional_title)
        persona.description = data.get('description', persona.description)
        persona.age = data.get('age', persona.age)
        persona.gender = data.get('gender', persona.gender)
        persona.occupation = data.get('occupation', persona.occupation)
        persona.quote_summarized = data.get('quote_summarized', persona.quote_summarized)
        db.session.commit()
        return jsonify({'message': 'Persona updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@personas_bp.route('/personas-delete/<int:id>', methods=['DELETE'])
def delete_persona(id):
    persona = PersonasBaseData.query.get_or_404(id)
    try:
        db.session.delete(persona)
        db.session.commit()
        return jsonify({'message': 'Persona deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@personas_bp.route('/persona/<int:persona_id>', methods=['GET'])
def view_persona(persona_id):
    """Retrieve the persona details and render the persona page"""
    persona = PersonasBaseData.query.get_or_404(persona_id)

    persona_data = {
        "id": persona.id,
        "photo": persona.photo,
        "name": persona.name,
        "additional_title": persona.additional_title,
        "description": persona.description,
        "age": persona.age,
        "gender": persona.gender,
        "occupation": persona.occupation,
        "quote_summarized": persona.quote_summarized,
        "created_at": persona.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": persona.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        "goals": [persona.goals[0].goal_01, persona.goals[0].goal_02, persona.goals[0].goal_03] if persona.goals else [],
        "motivations": [persona.motivations[0].motivation_01, persona.motivations[0].motivation_02, persona.motivations[0].motivation_03] if persona.motivations else [],
        "frustrations": [persona.frustrations[0].frustration_01, persona.frustrations[0].frustration_02, persona.frustrations[0].frustration_03] if persona.frustrations else [],
        "activities": [persona.activities[0].activity_01, persona.activities[0].activity_02, persona.activities[0].activity_03, persona.activities[0].activity_04, persona.activities[0].activity_05] if persona.activities else [],
        "digital_use": {
            "desktop_use": persona.digital_use[0].desktop_use if persona.digital_use else "Not known",
            "mobile_use": persona.digital_use[0].mobile_use if persona.digital_use else "Not known",
            "social_media_use": persona.digital_use[0].social_media_use if persona.digital_use else "Not known",
            "computer_literacy": persona.digital_use[0].computer_literacy if persona.digital_use else "Not known",
            "frequently_used_tools_and_apps": persona.digital_use[0].frequently_used_tools_and_apps if persona.digital_use else "Not known"
        },
        "persona_quotes": [persona.persona_quotes[0].quote_01, persona.persona_quotes[0].quote_02, persona.persona_quotes[0].quote_03] if persona.persona_quotes else []
    }

    return render_template("persona.html", persona=persona_data)
