import requests
from enum import Enum


api_url = 'https://api.edamam.com/search'
api_id = '3eba0cf0'
app_key = '588df720c81ad61b51f639ce40386a14'


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class mealType(ExtendedEnum):
    lunch = 'lunch'
    dinner = 'dinner'
    breakfast = 'breakfast'
    snack = 'snack'


def get_recipe_info(recipe_name, meal_type=mealType.lunch, index=0):
    params = {
        'q': recipe_name,
        'app_id': api_id,
        'app_key': app_key,
        'diet': 'balanced',
        'mealType': meal_type,
    }

    res = requests.get(api_url, params=params)
    data = res.json()

    return dict({
        'label': data["hits"][index]["recipe"]["label"],
        'image': data["hits"][index]["recipe"]["image"],
        'recipe_url': data["hits"][index]["recipe"]["url"]})


def print_weather(city_name):
    api_url = 'http://api.openweathermap.org/data/2.5/weather'
    api_id = 'c65f3f0e16d0827d1fc4d460971feeb4'

    params = {
        'q': city_name,
        'appid': api_id,
        'units': 'metric'
    }

    res = requests.get(api_url, params=params)
    data = res.json()
    if data["cod"] != 404:
        print(data["main"]["temp"])
    else:
        print("Incorrect city name")