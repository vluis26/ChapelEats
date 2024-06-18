from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from openai import OpenAI
import certifi
import pandas as pd
import json
from dotenv import load_dotenv
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Initialize OpenAI client
client_AI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
load_dotenv()



mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client.get_database("ChapelEatsDB")
users_collection = db.get_collection("users")
meals_collection = db.get_collection("saved_meals")

csv_file_path = os.path.join(os.path.dirname(__file__), 'rams-head-dining-hall.csv')
food_data = pd.read_csv(csv_file_path)
food_data.columns = ['Meal Time', 'Food Item', 'Calories', 'Protein (g)', 'Fat (g)','Carbohydrates (g)','Organic', 'Vegetarian','Gluten Free' , 'Vegan']

app.config['ENV'] = 'production'
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if users_collection.find({"email": email}):
        return jsonify({'message': 'User already exists'}), 400

    user = {'name': name, 'email': email, 'password': password}
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully', 'name': user['name'], 'email': user['email']}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = users_collection.find_one({"email": email, "password": password})
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'name': user['name'], 'email': user['email']}), 200



def filter_foods_by_preferences(preferences):
    filtered_foods = food_data.copy()
    
    if preferences.get('dietaryRestrictions') == 'vegan':
        filtered_foods = filtered_foods[filtered_foods['Vegan'] == True]
    elif preferences.get('dietaryRestrictions') == 'vegetarian':
        filtered_foods = filtered_foods[filtered_foods['Vegetarian'] == True]
    elif preferences.get('dietaryRestrictions') == 'gluten_free':
        filtered_foods = filtered_foods[filtered_foods['Gluten Free'] == True]


    return filtered_foods


@app.route('/generate-meal', methods=['POST'])
def generate_meal():
    data = request.json

    preferences = {
        'nutritionalGoals': data.get('nutritionalGoals'),
        'dietaryRestrictions': data.get('dietaryRestrictions'),
        'sex': data.get('sex'),
        'mealTime': data.get('mealTime'),
        'diningHall': data.get('diningHall'),
        'age': data.get('age'),
        'height': data.get('height'),
        'weight': data.get('weight')
    }

    filtered_foods = filter_foods_by_preferences(preferences)

    meal_time = preferences['mealTime'].lower()

    if meal_time == 'breakfast':
        meal_foods = filtered_foods[filtered_foods['Meal Time'] == 'Breakfast']
    elif meal_time == 'lunch':
        meal_foods = filtered_foods[filtered_foods['Meal Time'] == 'Lunch']
    elif meal_time == 'dinner':
        meal_foods = filtered_foods[filtered_foods['Meal Time'] == 'Dinner']
    else:
        return jsonify({'message': f'Invalid meal time: {meal_time}'}), 400

    if meal_foods.empty:
        return jsonify({'message': f'No available options for {meal_time}'}), 404

    food_list = meal_foods.to_dict('records')

    # Truncate the food list
    max_items = 150  # Adjust this number as needed
    if len(food_list) > max_items:
        food_list = food_list[:max_items]

    prompt = f"Generate a {meal_time} meal plan for a {preferences} diet using the following food options: {json.dumps(food_list)}"
    response = client_AI.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=450
    )

    meal_description = response.choices[0].message.content.strip()

    # Calculate the total nutritional values
    total_calories = sum(item['Calories'] for item in food_list)
    total_protein = sum(item['Protein (g)'] for item in food_list)
    total_fat = sum(item['Fat (g)'] for item in food_list)
    total_carbs = sum(item['Carbohydrates (g)'] for item in food_list)

    nutritional_info = {
        'Total Calories': total_calories,
        'Total Protein (g)': total_protein,
        'Total Fat (g)': total_fat,
        'Total Carbohydrates (g)': total_carbs
    }

    return jsonify({
        'meal_description': meal_description,
        'nutritional_info': nutritional_info
    }), 200


@app.route('/save-meal', methods=['POST'])
def save_meal():
    data = request.json
    print("Received data:", data)  # Log the received data

    email = data.get('email')
    meal_description = data.get('meal_description')
    nutritional_info = data.get('nutritional_info', {})  # Provide a default empty dictionary

    print("Email:", email)
    print("Meal Description:", meal_description)
    print("Nutritional Info:", nutritional_info)

    if not email or not meal_description or not nutritional_info:
        return jsonify({'message': 'Missing required fields'}), 400

    meal = {
        'email': email,
        'meal_description': meal_description,
        'nutritional_info': nutritional_info
    }

    try:
        meals_collection.insert_one(meal)
        return jsonify({'message': 'Meal saved successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to save meal', 'error': str(e)}), 500


@app.route('/get-saved-meals', methods=['GET'])
def get_saved_meals():
    email = request.args.get('email')
    print(email)
    if not email:
        return jsonify({'message': 'Missing required fields'}), 400

    saved_meals = list(meals_collection.find_one({'email': email}, {'_id': 0}))

    return jsonify({'savedMeals': saved_meals}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
