# import requests
# from bs4 import BeautifulSoup

# def fetch_recipe_info(recipe_id):
#     # Step 1: Send a GET request to fetch the JSON data
#     url = f"https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php?recipe={recipe_id}"
#     response = requests.get(url)
#     data = response.json()

#     # Step 2: Extract the HTML content from the JSON response
#     html_content = data.get("html", "")

#     # Step 3: Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Step 4: Extract specific data

#     # Recipe name
#     recipe_name = soup.find('h2').text if soup.find('h2') else "No recipe name found"

#     # Allergens
#     allergens = ""
#     allergens_header = soup.find('h6', text='Allergens')
#     if allergens_header:
#         allergens = allergens_header.find_next('p').text
#     else:
#         allergens = "No allergens information"

#     # Nutritional information
#     nutrition_table = soup.find('table', class_='nutrition-facts-table')
#     nutrition_info = {}

#     if nutrition_table:
#         for row in nutrition_table.find_all('tr', class_='main-line'):
#             cells = row.find_all(['th', 'td'])
#             if len(cells) == 3:
#                 nutrient = cells[0].text.strip()
#                 amount = cells[1].text.strip()
#                 nutrition_info[nutrient] = amount
#             elif len(cells) == 2:
#                 nutrient = cells[0].text.strip()
#                 amount = cells[1].text.strip()
#                 nutrition_info[nutrient] = amount

#         for row in nutrition_table.find_all('tr'):
#             if 'class' not in row.attrs or 'main-line' not in row.attrs['class']:
#                 cells = row.find_all(['th', 'td'])
#                 if len(cells) == 3:
#                     nutrient = cells[1].text.strip()
#                     amount = cells[0].text.strip()
#                     nutrition_info[nutrient] = amount

#     return {
#         "recipe_name": recipe_name,
#         "allergens": allergens,
#         "nutrition_info": nutrition_info
#     }