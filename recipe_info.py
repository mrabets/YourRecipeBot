import requests
from enum_classes import *


import json

# Recipe Search API Documentation https://developer.edamam.com/edamam-docs-recipe-api

api_url = 'https://api.edamam.com/search'
api_id = '3eba0cf0'
app_key = '588df720c81ad61b51f639ce40386a14'

# JSON file move
recipe_index = -1


def write_recipe_info_to_file(recipe_name,
                              diet,
                              cuisine_type,
                              meal_type,
                              dish_type,
                              calories,
                              time):
    params = {
        'q': recipe_name,
        'app_id': api_id,
        'app_key': app_key,
        'diet': diet.lower(),
        'cuisineType': cuisine_type,
        'mealType': meal_type,
        'dishType': dish_type,
        'calories': f'0-{calories}',
        'time': f'0-{time}'
    }
    global recipe_index
    recipe_index = -1
    res = requests.get(api_url, params=params)
    data = res.json()

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)


def get_recipe_url():
    with open('data.json') as json_file:
        data = json.load(json_file)
    global recipe_index
    recipe_index += 1
    if recipe_index >= len(data["hits"]):
        return None
    return data["hits"][recipe_index]["recipe"]["url"]
