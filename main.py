import telebot
from telebot import types
from enum_classes import *
from recipe_info import write_recipe_info_to_file
from recipe_info import get_recipe_url
from config import ACCESS_TOKEN

bot = telebot.TeleBot(ACCESS_TOKEN)

recipe_dict = {}


class Recipe:
    def __init__(self, name):
        self.name = name
        self.diet = None
        self.cuisine_type = None
        self.meal_type = None
        self.dish_type = None
        self.calories = None
        self.time = None


@bot.message_handler(commands=['start', 'recipe'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Chicken', 'Fish', 'Fruit', 'Vegetables', 'Nuts', 'Dairy')
    msg = bot.reply_to(message, """\
        Hi! I'm YourRecipeBot. Let's search your ideal recipe. Follow me!
        What's your recipe name?
        """, reply_markup=markup)
    bot.register_next_step_handler(msg, process_recipe_name_step)


def process_recipe_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        recipe = Recipe(name)
        recipe_dict[chat_id] = recipe

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(*DietLabels.list())
        markup.add('Go back')
        msg = bot.reply_to(message, 'What\'s the diet?',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_diet_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_diet_step(message):
    try:
        chat_id = message.chat.id
        recipe = recipe_dict[chat_id]
        if message.text == u'Go back':
            send_welcome(message)
            return
        diet = message.text
        # if diet in [u'Balanced', u'High-protein', u'High-fiber', u'Low-fat', u'Low-sodium']:
        if diet in DietLabels.list():
            recipe.diet = diet
        else:
            raise Exception("Unknown diet")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(*CuisineType.list())
        markup.add('Go back')
        msg = bot.reply_to(message, 'What\'s the cuisine type?',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_cuisine_type_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_cuisine_type_step(message):
    try:
        chat_id = message.chat.id
        recipe = recipe_dict[chat_id]
        if message.text == u'Go back':
            process_recipe_name_step(message)
            return
        cuisine_type = message.text
        if cuisine_type in CuisineType.list():
            recipe.cuisine_type = cuisine_type
        else:
            raise Exception("Unknown cuisine type")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(*MealType.list())
        markup.add('Go back')
        msg = bot.reply_to(message, 'What\'s the meal type?',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_meal_type_step)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_meal_type_step(message):
    try:
        chat_id = message.chat.id
        recipe = recipe_dict[chat_id]
        if message.text == u'Go back':
            message.text = recipe.diet
            process_diet_step(message)
            return
        mealType = message.text
        if mealType in MealType.list():
            recipe.meal_type = mealType
        else:
            raise Exception("Unknown meal type")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(*DishType.list())
        markup.add('Go back')
        msg = bot.reply_to(message, 'What\'s the dish type?',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_dish_type_step)

    except Exception as e:
        bot.reply_to(message, 'I can\'t find suitable recipe! Try /start again with other parameters\n')


def process_dish_type_step(message):
    try:
        chat_id = message.chat.id
        recipe = recipe_dict[chat_id]
        if message.text == u'Go back':
            message.text = recipe.cuisine_type
            process_cuisine_type_step(message)
            return
        dishType = message.text
        if dishType in DishType.list():
            recipe.dish_type = dishType
        else:
            raise Exception("Unknown dish type")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Go back')
        msg = bot.reply_to(message, 'How many calories? (kcal)',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_calories_step)

    except Exception as e:
        bot.reply_to(message, 'I can\'t find suitable recipe! Try /start again with other parameters\n')


def process_calories_step(message):
    try:
        chat_id = message.chat.id
        recipe = recipe_dict[chat_id]
        if message.text == u'Go back':
            message.text = recipe.meal_type
            process_meal_type_step(message)
            return
        calories = message.text
        if not calories.isdigit():
            msg = bot.reply_to(message, 'Calories should be a number. How many calories do you want?')
            bot.register_next_step_handler(msg, process_calories_step)
            return
        recipe.calories = calories
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Go back')
        msg = bot.reply_to(message, 'How many maximum сooking time? (min)',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, process_time_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_time_step(message):
    try:
        chat_id = message.chat.id
        recipe = recipe_dict[chat_id]
        if message.text == u'Go back':
            message.text = recipe.dish_type
            process_dish_type_step(message)
            return
        time = message.text
        if not time.isdigit():
            msg = bot.reply_to(message, 'Time should be a number.')
            bot.register_next_step_handler(msg, process_time_step)
            return
        recipe.time = time
        bot.send_message(chat_id, f"Ok. Your recipe: "
                                  f"\nName: {recipe.name}"
                                  f"\nDiet: {recipe.diet}"
                                  f"\nCuisine type: {recipe.cuisine_type}"
                                  f"\nMeal type: {recipe.meal_type}"
                                  f"\nDish type: {recipe.dish_type}"
                                  f"\nCalories: {recipe.calories} kcal"
                                  f"\nTime: {recipe.time} min")
        write_recipe_info_to_file(
            recipe_name=recipe.name,
            diet=recipe.diet,
            cuisine_type=recipe.cuisine_type,
            meal_type=recipe.meal_type,
            dish_type=recipe.dish_type,
            calories=recipe.calories,
            time=recipe.time
        )
        recipe_url = get_recipe_url()
        if recipe_url is None:
            bot.reply_to(message, 'Recipe list is empty!')
            bot.register_next_step_handler(message, process_finish_step)
            return
        bot.send_message(chat_id, 'Hey! I found something: \n ' + recipe_url)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        markup.add('Get another', 'Finish', 'Start over')
        msg = bot.reply_to(message, 'Do you want to get another?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_another_recipe_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_another_recipe_step(message):
    try:
        chat_id = message.chat.id
        answer = message.text
        recipe = recipe_dict[chat_id]
        if answer == u'Get another':
            recipe_url = get_recipe_url()
            if recipe_url is None:
                bot.reply_to(message, 'Recipe list is empty!')
                bot.register_next_step_handler(message, process_finish_step)
            else:
                bot.send_message(chat_id, 'I found something new: \n ' + recipe_url)
                bot.register_next_step_handler(message, process_another_recipe_step)
        elif answer == u'Start over':
            send_welcome(message)
            return
        elif answer == u'Finish':
            bot.register_next_step_handler(message, process_finish_step)
    except Exception as e:
        bot.reply_to(message, 'oooops!')


def process_finish_step(message):
    bot.send_message(message.chat.id, 'That\'s all! Thank you for using! Enter /start to repeat \n ',
                     reply_markup=types.ReplyKeyboardRemove())


bot.polling()
