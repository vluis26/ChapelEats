from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from openai import OpenAI
import certifi
import requests
from bs4 import BeautifulSoup

client_AI= OpenAI()

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

    # Return user's name along with the login message
    return jsonify({'message': 'Login successful', 'name': user['name'], 'email': user['email']}), 200



def fetch_recipe_info(recipe_id):
    print(f"Fetching recipe info for Recipe ID: {recipe_id}")
    url = f"https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php?recipe={recipe_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching recipe info: {response.status_code}")
        return {"error": "Error fetching recipe info"}
    
    data = response.json()
    html_content = data.get("html", "")
    soup = BeautifulSoup(html_content, 'html.parser')
    recipe_name = soup.find('h2').text if soup.find('h2') else "No recipe name found"
    allergens_header = soup.find('h6', text='Allergens')
    allergens = allergens_header.find_next('p').text if allergens_header else "No allergens information"
    nutrition_table = soup.find('table', class_='nutrition-facts-table')
    nutrition_info = {}
    if nutrition_table:
        for row in nutrition_table.find_all('tr', class_='main-line'):
            cells = row.find_all(['th', 'td'])
            if len(cells) == 3:
                nutrient = cells[0].text.strip()
                amount = cells[1].text.strip()
                nutrition_info[nutrient] = amount
            elif len(cells) == 2:
                nutrient = cells[0].text.strip()
                amount = cells[1].text.strip()
                nutrition_info[nutrient] = amount
        for row in nutrition_table.find_all('tr'):
            if 'class' not in row.attrs or 'main-line' not in row.attrs['class']:
                cells = row.find_all(['th', 'td'])
                if len(cells) == 3:
                    nutrient = cells[1].text.strip()
                    amount = cells[0].text.strip()
                    nutrition_info[nutrient] = amount
    print(f"Fetched Recipe Info: {recipe_name}, {allergens}, {nutrition_info}")
    return {
        "recipe_name": recipe_name,
        "allergens": allergens,
        "nutrition_info": nutrition_info
    }



@app.route('/generate-meal', methods=['POST'])
def generate_meal():
    data = request.json
    nutritionalGoals = data.get('nutritionalGoals')
    dietaryRestrictions = data.get('dietaryRestrictions')
    sex = data.get('sex')
    mealTime = data.get('mealTime')
    diningHall = data.get('diningHall')
    age = data.get('age')
    height = data.get('height')
    weight = data.get('weight')

    # Modify the prompt to request recipe IDs
    prompt = f"Generate a meal plan for a {age}-year-old {sex} who is {height} cm tall and weighs {weight} kg. The meal should meet the following nutritional goals: {nutritionalGoals} and dietary restrictions: {dietaryRestrictions}. It is for {mealTime} at {diningHall} dining hall. Include the recipe IDs for each meal item in the format 'Recipe ID: X'."

    try:
        response = client_AI.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        meal_description = response.choices[0].message.content.strip()
        print(f"Generated Meal Description: {meal_description}")

        # Extract recipe IDs from the meal description
        recipe_ids = extract_recipe_ids(meal_description)
        if not recipe_ids:
            return jsonify({'error': 'No Recipe IDs found in meal description'}), 400

        # Fetch recipe details for each recipe ID
        recipes_info = [fetch_recipe_info(recipe_id) for recipe_id in recipe_ids]

        return jsonify({
            'meal_description': meal_description,
            'recipes_info': recipes_info
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def extract_recipe_ids(meal_description):
    import re
    return re.findall(r"Recipe ID: (\d+)", meal_description)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
