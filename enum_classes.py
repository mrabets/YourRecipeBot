from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class MealType(ExtendedEnum):
    Lunch = 'Lunch'
    Dinner = 'Dinner'
    Breakfast = 'Breakfast'
    Snack = 'Snack'
    Teatime = 'Teatime'


class DietLabels(ExtendedEnum):
    Balanced = 'Balanced'
    HighProtein = 'High-protein'
    HighFiber = 'High-fiber'
    LowFat = 'Low-fat'
    LowCarb = 'Low-carb'
    LowSodium = 'Low-sodium'


class DishType(ExtendedEnum):
    BiscuitsAndCookies = 'Biscuits and cookies'
    Bread = 'Bread'
    Cereals = 'Cereals'
    CondimentsAndSauces = 'Condiments and sauces'
    Drinks = 'Drinks'
    Desserts = 'Desserts'
    Egg = 'Egg'
    MainCourse = 'Main course'
    Omelet = 'Omelet'
    Pancake = 'Pancake'
    Preps = 'Preps'
    Preserve = 'Preserve'
    Salad = 'Salad'
    Sandwiches = 'Sandwiches'
    Soup = 'soup'
    Starter = 'Starter'


class CuisineType(ExtendedEnum):
    American = 'American'
    Asian = 'Asian'
    British = 'British'
    Caribbean = 'Caribbean'
    CentralEurope = 'Central Europe'
    Chinese = 'Chinese'
    EasternEurope = 'Eastern Europe'
    French = 'French'
    Indian = 'Indian'
    Italian = 'Italian'
    Japanese = 'Japanese'
    Kosher = 'Kosher'
    Mediterranean = 'Mediterranean'
    Mexican = 'Mexican'
    MiddleEastern = 'Middle Eastern'
    Nordic = 'Nordic'
    SouthAmerican = 'South American'
    SouthEastAsian = 'South East Asian'
