# Recipe Search API Documentation https://developer.edamam.com/edamam-docs-recipe-api

import requests
import json

from config import API_URL, API_ID, API_KEY


class Moving(object):
    recipe_index = 0

    @staticmethod
    def increment_index():
        Moving.recipe_index += 1


def write_recipe_info_to_file(recipe_name,
                              diet,
                              cuisine_type,
                              meal_type,
                              dish_type,
                              calories,
                              time):
    params = {
        'q': recipe_name,
        'app_id': API_ID,
        'app_key': API_KEY,
        'diet': diet.lower(),
        'cuisineType': cuisine_type,
        'mealType': meal_type,
        'dishType': dish_type,
        'calories': f'0-{calories}',
        'time': f'0-{time}'
    }
    Moving.recipe_index = 0
    res = requests.get(API_URL, params=params)
    data = res.json()

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)


def get_recipe_url():
    with open('data.json') as json_file:
        data = json.load(json_file)
    Moving.increment_index()
    if Moving.recipe_index >= len(data["hits"]):
        return None
    return data["hits"][Moving.recipe_index]["recipe"]["url"]
