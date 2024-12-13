# add_data.py
from app import create_app, db
from app.models.users import User
from app.models.user_uploaded_data import UserUploadedData

# Create an app instance
app = create_app()

with app.app_context():  # Push the application context
    # Query all records from UserUploadedData
    uploaded_data_records = UserUploadedData.query.all()

    # Check if records are found
    if uploaded_data_records:
        print("Data in UserUploadedData table:")
        for record in uploaded_data_records:
            print(f"ID: {record.id}, User ID: {record.user_id}, Persona ID: {record.persona_id}, "
                  f"File Name: {record.file_name}, File Path: {record.file_path}, File Type: {record.file_type}, "
                  f"Content: {record.content}, Uploaded At: {record.uploaded_at}, Processed: {record.processed}")
    else:
        print("No records found in the UserUploadedData table.")
