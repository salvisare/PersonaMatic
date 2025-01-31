from flask import Blueprint, request, jsonify
from openai import OpenAI
from app.models.user_uploaded_data import UserUploadedData
from app.models.personas import (
    PersonasBaseData, PersonasBaseDataAI, PersonaMotivations, PersonaFrustrations,
    PersonaActivities, PersonaGoals, PersonaDigitalUse, PersonaQuotes
)
from app import db, OPENAI_API_KEY
from datetime import datetime
import logging
import json
import re

api_key = OPENAI_API_KEY

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads', methods=['POST'])
def upload_file():
    data = request.json
    try:
        file_name = data.get('file_name')
        if not file_name:
            return jsonify({"error": "File name is required"}), 400

        upload = UserUploadedData(
            user_id=data['user_id'],
            file_name=file_name,
            file_path=data.get('file_path'),
            file_type=data.get('file_type'),
            content=data['content'],
            uploaded_at=datetime.utcnow(),
            processed=data.get('processed', False)
        )

        db.session.add(upload)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'id': upload.id}), 201

    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 400


@uploads_bp.route('/uploads-retrieve', methods=['GET'])
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
        logging.error(f"Error deleting file: {str(e)}")
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
    logging.info(f"Content being processed: {content}")

    try:
        client = OpenAI(api_key=api_key)
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a UX researcher, user interviewer, and content analysis specialist."},
                {"role": "user", "content": f"Analyze the following content for the use of user persona and return a structured JSON object with these keys:\n"
                                            f"- name (if no name is provided in the content, use a random name and surname, avoing surnames Smith and Doe)\n"
                                            f"- additional title (use a partial occupation and partially emotional adjective depending on the content given)\n"
                                            f"- age\n"
                                            f"- gender (if no gender is given, provide the gender according to the generated name)\n"
                                            f"- summarized quote (a single sentence, mandatory, extract a prominent persona quote from the content given, be descriptive and use only one sentence)\n"
                                            f"- occupation\n"
                                            f"- description (generate a user persona description)\n"
                                            f"- goals (list of 3, if no goals are mentioned, generate goals according to the occupation and activities)\n"
                                            f"- motivations (list of 3, if no motivations are mentioned, generate motivations according to the occupation and description)\n"
                                            f"- frustrations (list of 3, if no frustrations are mentioned, generate typical frustrations for the relevant occupation)\n"
                                            f"- activities (list of 5, if no activities are mentioned, generate relevant activities based on the context or occupation)\n\n"
                                            f"- persona quotes (extract a list of 3 additional interesting persona quotes from the content provided, don't repeat the prominent quote)\n"
                                            f"- desktop use (output 'not known' if nothing is mentioned about desktop use)\n"
                                            f"- mobile use (output 'not known' if nothing is mentioned about mobile use)\n"
                                            f"- social media use (output 'not known' if nothing is mentioned about social media use)\n"
                                            f"- computer literacy (output 'not known' if nothing is mentioned about computer literacy)\n"
                                            f"- frequently used digital tools and apps (output 'not known' if nothing is mentioned about frequently used digital tools and apps)\n"
                                            f"Input Content:\n\n{content}\n\n"
                                            f"Output ONLY valid JSON format. Do not include any additional text, explanations, or commentary."}
            ],
            max_tokens=1000,
            response_format=PersonasBaseDataAI
        )

        response_content = response.choices[0].message.content
        print(response_content)
        logging.info(f"Raw OpenAI Response Content: {response_content}")

        # Attempt to parse JSON response
        try:
            processed_data = json.loads(response_content)
        except json.JSONDecodeError:
            logging.warning("Response is not JSON. Attempting manual extraction.")
            match = re.search(r"{.*}", response_content, re.DOTALL)
            if match:
                try:
                    processed_data = json.loads(match.group(0))
                except json.JSONDecodeError:
                    processed_data = {}
            else:
                processed_data = {}

        # Fallback to defaults if parsing fails
        if not processed_data:
            processed_data = {
                "name": "Unknown",
                "additional title": "Unknown",
                "age": 0,
                "gender": "No Gender",
                "description": "No Description",
                "occupation": "Unknown",
                "quote_summarized": "Unknown",
                "goals": ["General goal 1", "General goal 2", "General goal 3"],
                "motivations": ["General motivation 1", "General motivation 2", "General motivation 3"],
                "frustrations": ["General frustration 1", "General frustration 2", "General frustration 3"],
                "activities": ["General activity 1", "General activity 2", "General activity 3", "General activity 4", "General activity 5"],
                "persona quotes": ["Persona quote 1", "Persona quote 2", "Persona quote 3"],
                "desktop use": "Unknown",
                "mobile use": "Unknown",
                "social media use": "Unknown",
                "computer literacy": "Unknown",
                "frequently used digital tools and apps": "Unknown",
            }

        # Extract data
        name = processed_data.get("name", "Unknown")
        additional_title = processed_data.get("additional title", "Unknown")
        age = processed_data.get("age", 0)
        gender = processed_data.get("gender", "Unknown")
        description = processed_data.get("description", "No Description")
        occupation = processed_data.get("occupation", "Unknown")
        quote_summarized = processed_data.get("quote_summarized", "Unknown")
        goals = processed_data.get("goals", [])
        motivations = processed_data.get("motivations", [])
        frustrations = processed_data.get("frustrations", [])
        activities = processed_data.get("activities", [])
        persona_quotes = processed_data.get("persona_quotes", [])
        desktop_use = processed_data.get("desktop_use", "Unknown")
        mobile_use = processed_data.get("mobile_use", "Unknown")
        social_media_use = processed_data.get("social_media_use", "Unknown")
        computer_literacy = processed_data.get("computer_literacy", "Unknown")
        frequently_used_tools_and_apps = processed_data.get("frequently_used_digital_tools_and_apps", "Unknown")

        # Create persona object
        persona = PersonasBaseData(
            user_id=record.user_id,
            photo="default.jpg",
            name=name,
            additional_title=additional_title,
            description=description,
            age=age,
            gender=gender,
            occupation=occupation,
            quote_summarized=quote_summarized
        )
        db.session.add(persona)
        db.session.commit()

        # Save digital use
        db.session.add(PersonaDigitalUse(
            persona_id=persona.id,
            desktop_use=desktop_use,
            mobile_use=mobile_use,
            social_media_use=social_media_use,
            computer_literacy=computer_literacy,
            frequently_used_tools_and_apps=frequently_used_tools_and_apps,
        ))

        # Save goals
        db.session.add(PersonaGoals(
            persona_id=persona.id,
            goal_01=goals[0] if len(goals) > 0 else None,
            goal_02=goals[1] if len(goals) > 1 else None,
            goal_03=goals[2] if len(goals) > 2 else None,
        ))

        # Save motivations
        db.session.add(PersonaMotivations(
            persona_id=persona.id,
            motivation_01=motivations[0] if len(motivations) > 0 else None,
            motivation_02=motivations[1] if len(motivations) > 1 else None,
            motivation_03=motivations[2] if len(motivations) > 2 else None,
        ))

        # Save frustrations
        db.session.add(PersonaFrustrations(
            persona_id=persona.id,
            frustration_01=frustrations[0] if len(frustrations) > 0 else None,
            frustration_02=frustrations[1] if len(frustrations) > 1 else None,
            frustration_03=frustrations[2] if len(frustrations) > 2 else None,
        ))

        # Save activities
        db.session.add(PersonaActivities(
            persona_id=persona.id,
            activity_01=activities[0] if len(activities) > 0 else "No activity provided",
            activity_02=activities[1] if len(activities) > 1 else None,
            activity_03=activities[2] if len(activities) > 2 else None,
            activity_04=activities[3] if len(activities) > 3 else None,
            activity_05=activities[4] if len(activities) > 4 else None
        ))

        # Save frustrations
        db.session.add(PersonaQuotes(
            persona_id=persona.id,
            quote_01=persona_quotes[0] if len(persona_quotes) > 0 else None,
            quote_02=persona_quotes[1] if len(persona_quotes) > 1 else None,
            quote_03=persona_quotes[2] if len(persona_quotes) > 2 else None,
        ))

        db.session.commit()

        # Mark record as processed
        record.processed = True
        db.session.commit()

        return jsonify({
            "upload_id": upload_id,
            "persona_id": persona.id,
            "message": "Data processed and saved successfully",
            "processed_data": {
                "name": name,
                "additional title": additional_title,
                "age": age,
                "gender": gender,
                "occupation": occupation,
                "quote summarized": quote_summarized,
                "description": description,
                "goals": goals,
                "motivations": motivations,
                "frustrations": frustrations,
                "activities": activities,
                "persona quotes": persona_quotes,
                "desktop use": desktop_use,
                "mobile use": mobile_use,
                "social media use": social_media_use,
                "computer literacy": computer_literacy,
                "frequently used digital tools and apps": frequently_used_tools_and_apps,
            }
        })

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error processing content: {str(e)}")
        return jsonify({"error": str(e)}), 500


