# import requests
# import json

# # Define the URL of your Flask application
# url = 'http://localhost:8080/generate-meal'  # Update with your actual URL if different

# # Example data payload for the POST request
# data = {
#     'nutritionalGoals': 'Weight Loss',
#     'dietaryRestrictions': 'vegetarian',
#     'sex': 'female',
#     'mealTime': 'lunch',
#     'diningHall': 'Chase  Hall',
#     'age': 25,
#     'height': 160,
#     'weight': 55
# }

# # Convert data to JSON format
# headers = {'Content-Type': 'application/json'}
# json_data = json.dumps(data)

# # Send POST request
# response = requests.post(url, data=json_data, headers=headers)

# # Print response
# print(response.status_code)
# print(response.json())
