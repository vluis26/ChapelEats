from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import certifi

app = Flask(__name__)

# MongoDB connection URI
mongo_uri = "mongodb+srv://luisvilla122003:TCmNf457CIScy5vc@cluster5.katcvxg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client.get_database("ChapelEatsDB")  # Replace with your database name
users_collection = db.get_collection("users")

# Enable CORS for all routes and allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Simple validation
    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({'message': 'User already exists'}), 400

    # Save the user
    user = {'name': name, 'email': email, 'password': password}
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Simple validation
    if not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Find user
    user = users_collection.find_one({"email": email, "password": password})
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
