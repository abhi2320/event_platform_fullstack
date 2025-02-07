from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket setup

# Basic test route
@app.route('/')
def home():
    return jsonify(message="Event Platform API")

# Main entry point
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)