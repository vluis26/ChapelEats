from flask import Flask, jsonify, request
# from flask_cors import CORS

app = Flask(__name__)
# cors= CORS(app, origins='*')

users = [
]

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to ChapelEats!'}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password =data.get('password')

    # Validations
    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    
    # If user exists
    if any(user['email'] == email for user in users):
        return jsonify({'message': 'User already exists'}), 400

    # Save user
    user = {'name': name, 'email': email, 'password': password}
    users.append(user)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validation
    if not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Find user
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200



if __name__ == "__main__":
    app.run(debug=True, port=8080)