from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
