from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import bcrypt
from functools import wraps
from bson import ObjectId

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client.cluster0  # Use "cluster0" database

# JWT Configuration
JWT_ALGORITHM = "HS256"
JWT_SECRET = os.getenv("JWT_SECRET")

# Test route
@app.route('/')
def home():
    return jsonify(message="Event Platform API")

# Hash password before storing
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Check password during login
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ============== Authentication Middleware ============== #
def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]  # Returns user ID
    except Exception as e:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Missing token"}), 401
        
        try:
            token = token.split(" ")[1]  # Remove "Bearer" prefix
            user_id = verify_token(token)
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated

# ----------- Authentication Routes ----------- #
@app.post('/register')
def register():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email/password"}), 400
    
    existing_user = db.users.find_one({"email": data['email']})
    if existing_user:
        return jsonify({"error": "User already exists"}), 409
    
    user_data = {
        "email": data['email'],
        "password": hash_password(data['password']),  # Secure password
        "created_at": datetime.utcnow()
    }
    db.users.insert_one(user_data)
    
    return jsonify({"message": "User registered"}), 201
 
@app.post('/login')
def login():
    data = request.json
    user = db.users.find_one({"email": data['email']})
    
    if not user or not check_password(data['password'], user['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = jwt.encode(
        {"sub": str(user["_id"]), "exp": datetime.utcnow() + timedelta(hours=2)},
        JWT_SECRET, algorithm=JWT_ALGORITHM
    )
    
    return jsonify({"token": token})

# ============== Event Routes (Protected) ============== #
@app.post('/events')
@token_required  # Use the auth middleware
def create_event(user_id):
    data = request.json
    event = {
        "title": data['title'],
        "description": data['description'],
        "date": data['date'],
        "organizer": user_id,  # From JWT token
        "attendees": []
    }
    result = db.events.insert_one(event)
    return jsonify({"message": "Event created", "id": str(result.inserted_id)}), 201

@app.get('/events')
def get_events():
    events = list(db.events.find())
    # Convert ObjectId to string for JSON serialization
    for event in events:
        event['_id'] = str(event['_id'])
        event['organizer'] = str(event['organizer'])
    return jsonify(events)

@app.delete('/events/<event_id>')
@token_required
def delete_event(user_id, event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    if event['organizer'] != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    db.events.delete_one({"_id": ObjectId(event_id)})
    return jsonify({"message": "Event deleted"}), 200

@app.post('/events/<event_id>/register')
@token_required
def register_attendee(user_id, event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    if user_id in event["attendees"]:
        return jsonify({"error": "Already registered"}), 400
    
    db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$push": {"attendees": user_id}}
    )
    
    socketio.emit("update_attendees", {"event_id": event_id, "count": len(event["attendees"]) + 1})
    
    return jsonify({"message": "Registered successfully"})

@app.route("/events/attendees/<event_id>")
def get_attendees(event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    return jsonify({"attendees": len(event["attendees"])})

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)