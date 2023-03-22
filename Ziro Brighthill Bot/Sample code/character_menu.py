import config
import telebot
# Импортируем модуль для создания объектов InlineKeyboardMarkup и InlineKeyboardButton
from telebot import types

# Создаем объект бота с помощью токена, полученного от @BotFather
bot = telebot.TeleBot(config.tg_token)

# Создаем словарь для хранения данных пользователей
user_data = {}

# Определяем константы для разных команд меню
MENU_CREATE_CHARACTER = "Создать персонажа"
MENU_SHOW_CHARACTER = "Показать персонажа"
MENU_DELETE_CHARACTER = "Удалить персонажа"

# Определяем обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    # Отправляем приветственное сообщение пользователю
    bot.send_message(message.chat.id, "Привет! Давай создадим игровой мир вместе.")
    # Переходим к следующему шагу - выбору команды меню 
    menu(message.chat.id)

# Определяем функцию для отображения меню с командами 
def menu(chat_id):
    # Создаем объект InlineKeyboardMarkup для отображения кнопок с выбором команды 
    keyboard = types.InlineKeyboardMarkup()
    # Создаем объекты InlineKeyboardButton для каждой команды и добавляем их к клавиатуре 
    button_create = types.InlineKeyboardButton(text=MENU_CREATE_CHARACTER,
                                               callback_data=MENU_CREATE_CHARACTER)
    button_show = types.InlineKeyboardButton(text=MENU_SHOW_CHARACTER,
                                             callback_data=MENU_SHOW_CHARACTER)
    button_delete = types.InlineKeyboardButton(text=MENU_DELETE_CHARACTER,
                                               callback_data=MENU_DELETE_CHARACTER)
    keyboard.add(button_create, button_show, button_delete)
    # Отправляем сообщение с клавиатурой и просим пользователя выбрать команду  
    bot.send_message(chat_id,
                     "Выбери одну из предложенных команд или напиши свою.",
                     reply_markup=keyboard)

# Определяем обработчик всех текстовых сообщений 
@bot.message_handler(content_types=["text"])
def text(message):
    # Проверяем, есть ли данные пользователя в словаре 
    if message.from_user.id in user_data:
        # Получаем данные пользователя из словаря 
        data = user_data[message.from_user.id]
        # Проверяем, какой шаг ожидает бот от пользователя 
        if data["step"] == "name":
            # Сохраняем ответ пользователя в поле name 
            data["name"] = message.text 
            # Выводим ответ пользователя в консоль (можно удалить эту строку) 
            print(data["name"]) 
            # Переходим к следующему шагу - описанию персонажа 
            description(message.from_user.id) 

        elif data["step"] == "description":
            # Сохраняем ответ пользователя в поле description  
            data["description"] = message.text  
            # Выводим ответ пользователя в консоль (можно удалить эту строку)  
            print(data["description"])  
            # Отправляем сообщение пользователю с подтверждением создания персонажа   
            bot.send_message(message.from_user.id,
                             f"Спасибо! Я создал твоего персонажа: \nИмя: {data['name']}\nОписание: {data['description']}")
            # Сбрасываем данные пользователя из словаря  
            user_data.pop(message.chat.id) 
    else:
        # Если пользователь не ввел команду /start или не ответил на вопросы, то игнорируем его сообщение  
        pass

# Запускаем бота 
bot.polling()