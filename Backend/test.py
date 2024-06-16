from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/save-meal', methods=[])
def save_meal():
    data = request.json
    email = data.get('email')
    meal_description = data.get('meal_description')
    nutritional_info = data.get('nutritional_info')

    print(email)
    print(meal_description)
    print(nutritional_info)
    if not email or not meal_description or not nutritional_info:
        return jsonify({'message': 'Missing required fields'}),400

    return jsonify({'message': 'Meal saved successfully'}),201
