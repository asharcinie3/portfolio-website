import os
from flask_app import create_app, socketio

app = create_app(debug=False)

# For local development
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# For Gunicorn - just export the Flask app
application = app