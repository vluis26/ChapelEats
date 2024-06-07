from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from openai import OpenAI
import certifi

client = OpenAI(api_key= "")


app = Flask(__name__)

mongo_uri = "mongodb+srv://luisvilla122003:TCmNf457CIScy5vc@cluster5.katcvxg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client.get_database("ChapelEatsDB")
users_collection = db.get_collection("users")


CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    preferances = data.get('preferances', {})

    # Simple validation
    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({'message': 'User already exists'}), 400

    # Save the user
    user = {'name': name, 'email': email, 'password': password, 'preferances': preferances}
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

    # Return user's name along with the login message
    return jsonify({'message': 'Login successful', 'name': user['name'], 'email': user['email'],'preferences': user.get('preferences', {})}), 200

# @app.route('/get-preferences', methods=['POST'])
# def get_preferences():
#     data = request.json
#     email = data.get('email')
#     user = users_collection.find_one({"email": email})
#     if user:
#         preferences = {
#             "nutritionalGoals": user.get("nutritionalGoals", ""),
#             "dietaryRestrictions": user.get("dietaryRestrictions", ""),
#             "sex": user.get("sex", ""),
#             "mealTime": user.get("mealTime", ""),
#             "diningHall": user.get("diningHall", ""),
#             "age": user.get("age", ""),
#             "height": user.get("height", ""),
#             "weight": user.get("weight", "")
#         }
#         return jsonify({"preferences": preferences}), 200
#     else:
#         return jsonify({"error": "User not found"}), 404

# @app.route('/generate-meal', methods=['POST'])
# def generate_meal():
#     data = request.json
#     email = data.get('email')
#     print("Received email:", email)  # Add this line for debugging

#     # Find User
#     user = users_collection.find_one({"email": email})
#     print("User:", user)  # Add this line for debugging
#     if not user:
#         return jsonify({'message': 'User not found'}), 404

#     preferences = user.get('preferences', {})
#     print("User Preferences:", preferences)  # Add this line for debugging

#     # OpenAI API
#     prompt = f"Generate a meal plan based on the following preferences: {preferences}"
#     response = client.Completion.create(
#         engine="davinci-codex",
#         prompt=prompt,
#         max_tokens=150
#     )

#     meal_plan = response.choices[0].text.strip()
#     return jsonify({'meal_plan': meal_plan}), 200







if __name__ == "__main__":
    app.run(debug=True, port=8080)
