# Импортируем модуль для работы с телеграм-ботом
import telebot
import config
# Импортируем модуль для создания объектов InlineKeyboardMarkup и InlineKeyboardButton
from telebot import types

# Создаем объект бота с помощью токена, полученного от @BotFather
bot = telebot.TeleBot(config.tg_token)
user_data = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Фэнтези'), types.KeyboardButton('Средневековье'), types.KeyboardButton("Вестерн"))
    bot.reply_to(message, "Ты выбрал сеттинг:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if 'settings' not in user_data[chat_id]:
        user_data[chat_id]['settings'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('Орк'), types.KeyboardButton('Гном'), types.KeyboardButton('Эльф'))
        bot.reply_to(message, "Ты выбрал персонажа:", reply_markup=markup)
    elif 'character' not in user_data[chat_id]:
        user_data[chat_id]['character'] = message.text
        msg = bot.reply_to(message, "Опиши своего персонажа:")
        bot.register_next_step_handler(msg, process_character_description)
    else:
        process_expectations(message)


def process_character_description(message):
    chat_id = message.chat.id
    user_data[chat_id]['character_description'] = message.text
    bot.send_message(chat_id, "Хорошо, теперь опиши пожелания к игровой сессии:", reply_markup=None)
    bot.register_next_step_handler(message, process_wishes)


def process_wishes(message):
    chat_id = message.chat.id
    user_data[chat_id]['wishes'] = message.text
    msg = bot.reply_to(message, "Теперь опиши какой бы ты хотел экспириенс получить по мере игрового процесса:")
    bot.register_next_step_handler(msg, process_expectations)


def process_expectations(message):
    chat_id = message.chat.id
    user_data[chat_id]['expectations'] = message.text
    send_results(message.chat.id)


def send_results(user_id):
    chat_id = user_id
    result = f'Сеттинг: {user_data[chat_id]["settings"]}' \
             f'\nПерсонажи: {user_data[chat_id]["character"]}' \
             f'\nОписание персонажа: {user_data[chat_id]["character_description"]}' \
             f'\nПожелания к игровой сессии: {user_data[chat_id]["wishes"]}' \
             f'\nПользовательский экспириенс: {user_data[chat_id]["expectations"]}'
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id, result, reply_markup=markup)


# Запускаем бота
bot.polling()
