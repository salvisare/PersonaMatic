from flask import Blueprint, request, jsonify
from app.models.user_uploaded_data import UserUploadedData
from app import db
from datetime import datetime

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
