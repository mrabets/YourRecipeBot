import telebot
from telebot import types
from recipe_info import get_recipe_info

API_TOKEN = '1806049656:AAHZoSu4ObbtCrdnTZ-y8nJVOJvawe_Guhc'
BOT_URL = 'https://yourrecipebot.herokuapp.com/'

bot = telebot.TeleBot(API_TOKEN)

recipe_dict = {}


class Recipe:
    def __init__(self, name):
        self.name = name
        self.calories = None
        self.mealType = None


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('chicken', 'meat', 'fish')
    msg = bot.reply_to(message, """\
        Hi there, I am YourRecipe bot.
        What's your recipe name?
        """, reply_markup=markup)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        recipe = Recipe(name)
        recipe_dict[chat_id] = recipe
        msg = bot.reply_to(message, 'How many calories do you want?')
        bot.register_next_step_handler(msg, process_calories_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_calories_step(message):
    try:
        chat_id = message.chat.id
        calories = message.text
        if not calories.isdigit():
            msg = bot.reply_to(message, 'Calories should be a number. How many calories do you want?')
            bot.register_next_step_handler(msg, process_calories_step)
            return
        recipe = recipe_dict[chat_id]
        recipe.calories = calories
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('lunch', 'breakfast', 'dinner')
        msg = bot.reply_to(message, 'What is your meal type?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_meal_type_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_meal_type_step(message):
    try:
        chat_id = message.chat.id
        mealType = message.text
        recipe = recipe_dict[chat_id]
        if (mealType == u'lunch') or (mealType == u'breakfast') or (mealType == u'dinner'):
            recipe.mealType = mealType
        else:
            raise Exception("Unknown meal type")
        bot.send_message(chat_id, 'Ok, your recipe: ' + recipe.name + '\n Calories:' + str(recipe.calories) + '\n Meal type:' + recipe.mealType)
        recipe_url = get_recipe_info(recipe.name, recipe.mealType)['recipe_url']
        bot.send_message(chat_id, 'Hey! I found something: \n ' + recipe_url)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
