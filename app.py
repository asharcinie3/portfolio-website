import os
from flask_app import create_app, socketio

app = create_app(debug=True)

# This ensures the app runs correctly whether invoked directly or through a WSGI server
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
else:
    # This is important for Cloud Run and other WSGI servers
    # It creates the 'application' variable that many WSGI servers look for
    application = socketio