from flask import Blueprint, request, jsonify
from openai import OpenAI
from pydantic import BaseModel

from app.models.user_uploaded_data import UserUploadedData
from app.models.personas import PersonasBaseData, PersonasBaseDataAI, PersonaMotivations, PersonaFrustrations, PersonaActivities, PersonaGoals, PersonaDigitalUse, PersonaQuotes
from app import db, OPENAI_API_KEY
from datetime import datetime
import logging

api_key = OPENAI_API_KEY

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads', methods=['POST'])
def upload_file():
    data = request.json
    try:
        # Assuming the file name is part of the data
        file_name = data.get('file_name')  # Ensure this is passed in the JSON
        if not file_name:
            return jsonify({"error": "File name is required"}), 400

        upload = UserUploadedData(
            user_id=data['user_id'],
            file_name=file_name,  # Ensure file_name is provided
            file_path=data.get('file_path'),  # Optional if provided
            file_type=data.get('file_type'),  # Optional if provided
            content=data['content'],
            uploaded_at=datetime.utcnow(),
            processed=data.get('processed', False)
        )

        db.session.add(upload)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'id': upload.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@uploads_bp.route('/uploads-retrieve', methods=['GET']) #!!! update endpoint !!!
def retrieve_uploads():
    uploads = UserUploadedData.query.all()
    results = [
        {
            'id': u.id,
            'user_id': u.user_id,
            'content': u.content,
            'uploaded_at': u.uploaded_at,
            'processed': u.processed
        }
        for u in uploads
    ]
    return jsonify(results), 200


@uploads_bp.route('/uploads-retrieve/<int:id>', methods=['GET'])
def retrieve_upload(id):
    upload = UserUploadedData.query.get_or_404(id)
    return jsonify({
        'id': upload.id,
        'user_id': upload.user_id,
        'content': upload.content,
        'uploaded_at': upload.uploaded_at,
        'processed': upload.processed
    }), 200


@uploads_bp.route('/uploads-delete/<int:id>', methods=['DELETE'])
def delete_upload(id):
    upload = UserUploadedData.query.get_or_404(id)
    try:
        db.session.delete(upload)
        db.session.commit()
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@uploads_bp.route('/process-content', methods=['POST'])
def process_content():
    logging.info("Received request to process content.")

    upload_id = request.json.get('id')
    if not upload_id:
        return jsonify({"error": "ID is required"}), 400

    record = UserUploadedData.query.get(upload_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    content = record.content

    try:
        client = OpenAI(api_key=api_key)
        # Using openai.Completion.create() for new interface
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a UX researcher, user interviewer and content conceptualisation and interview analysis specialist."},    # now the role is developer instead system
                {"role": "user", "content": f"Analyze the following content and extract:\n"
                                            f"- Name, Age, Occupation, Description\n"
                                            f"- Top 3 Motivations\n"
                                            f"- Top 3 Frustrations\n"
                                            f"- Top 5 Activities\n"
                                            f"- Top 3 Goals (personal and professional):\n\n"
                                            f"{content}"}
            ],
            max_tokens=1000,    # restricting the model; now the tokens is max_completion_tokens 'check' instead max_tokens
            response_format=PersonasBaseDataAI
        )

        # Extract the generated content from the response
        # processed_data = response['choices'][0]['message']['content'].strip()
        processed_data = response.choices[0].message.parsed

        # Assuming OpenAI returns a structured JSON-like string
        # try:
        #     processed_json = eval(processed_data)  # Use `eval` cautiously or replace with `json.loads` if JSON
        # except Exception as e:
        #     return jsonify({"error": f"Failed to parse OpenAI response: {str(e)}"}), 500

        # Extract data from the processed JSON
        # name = processed_json.get('name')
        # age = processed_json.get('age')
        # occupation = processed_json.get('occupation')
        # description = processed_json.get('description')
        #
        # motivations = processed_json.get('motivations', [])
        # frustrations = processed_json.get('frustrations', [])
        # activities = processed_json.get('activities', [])
        # goals = processed_json.get('goals', [])

        # Insert into personas_base_data
        # persona = PersonasBaseData(
        #     user_id=record.user_id,
        #     name=name,
        #     age=age,
        #     occupation=occupation,
        #     description=description
        # )
        # db.session.add(persona)
        # db.session.commit()  # Commit to get persona ID
        #
        # # Insert into related tables
        # if motivations:
        #     for motivation in motivations:
        #         db.session.add(PersonaMotivations(persona_id=persona.id, motivation_01=motivation))
        # if frustrations:
        #     for frustration in frustrations:
        #         db.session.add(PersonaFrustrations(persona_id=persona.id, frustration_01=frustration))
        # if activities:
        #     for activity in activities[:5]:  # Limit to top 5
        #         db.session.add(PersonaActivities(persona_id=persona.id, activity_01=activity))
        # if goals:
        #     for goal in goals[:3]:  # Limit to top 3
        #         db.session.add(PersonaGoals(persona_id=persona.id, goal_01=goal))

    #     db.session.commit()
    #
    #     # Mark record as processed
    #     record.processed = True
    #     db.session.commit()
    #
        #print(processed_data["motivations"])
        return jsonify({
            "upload_id": upload_id,
            # "persona_id": persona.id,
            # "message": processed_data,
            "name": processed_data.name,
            "age": processed_data.age,
            "occupation": processed_data.occupation,
            "description": processed_data.description,
            "goals": processed_data.goals,
            "motivations": processed_data.motivations,
            "frustrations": processed_data.frustrations,
            "activities": processed_data.activities
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

