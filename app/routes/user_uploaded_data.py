from flask import Blueprint, request, jsonify
from app.models.user_uploaded_data import UserUploadedData
from app import db

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/api/uploads', methods=['POST'])
def upload_file():
    data = request.json
    try:
        upload = UserUploadedData(
            user_id=data['user_id'],
            file_name=data['file_name'],
            file_path=data['file_path'],
            file_type=data['file_type'],
            content=data['content'],
            processed=data.get('processed', False)
        )
        db.session.add(upload)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully', 'id': upload.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@uploads_bp.route('/api/uploads', methods=['GET'])
def retrieve_uploads():
    uploads = UserUploadedData.query.all()
    results = [
        {
            'id': u.id,
            'user_id': u.user_id,
            'file_name': u.file_name,
            'file_path': u.file_path,
            'file_type': u.file_type,
            'content': u.content,
            'uploaded_at': u.uploaded_at,
            'processed': u.processed
        }
        for u in uploads
    ]
    return jsonify(results), 200

@uploads_bp.route('/api/uploads/<int:id>', methods=['GET'])
def retrieve_upload(id):
    upload = UserUploadedData.query.get_or_404(id)
    return jsonify({
        'id': upload.id,
        'user_id': upload.user_id,
        'file_name': upload.file_name,
        'file_path': upload.file_path,
        'file_type': upload.file_type,
        'content': upload.content,
        'uploaded_at': upload.uploaded_at,
        'processed': upload.processed
    }), 200

@uploads_bp.route('/api/uploads/<int:id>', methods=['DELETE'])
def delete_upload(id):
    upload = UserUploadedData.query.get_or_404(id)
    try:
        db.session.delete(upload)
        db.session.commit()
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
