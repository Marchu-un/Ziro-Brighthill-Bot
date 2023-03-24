# Импортируем модуль для работы с телеграм-ботом
import telebot
import config
# Импортируем модуль для создания объектов InlineKeyboardMarkup и InlineKeyboardButton
from telebot import types

# Создаем объект бота с помощью токена, полученного от @BotFather
bot = telebot.TeleBot(config.tg_token)

# Создаем словарь для хранения данных пользователя
user_data = {}
data = {}

# Определяем константы для разных сеттингов
SETTING_FANTASY = "Фэнтези"
SETTING_SCI_FI = "Научная фантастика"
SETTING_HORROR = "Ужасы"
SETTING_MYSTERY = "Детектив"

# Определяем константы для разных команд меню
MENU_ADD_CHARACTER = "Добавить нового персонажа"
MENU_WISHES = "Описать пожелания к сессии"

# Определяем константы для разных step
STEP_SETTING = "setting"
STEP_CHARACTER = ""

# Определяем обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    # Отправляем приветственное сообщение пользователю
    bot.send_message(message.chat.id, "Привет! Давай создадим игровой мир вместе.")
    # Создаем объект InlineKeyboardMarkup для отображения кнопок с выбором сеттинга
    keyboard = types.InlineKeyboardMarkup()
    # Создаем объекты InlineKeyboardButton для каждого сеттинга и добавляем их к клавиатуре
    button_fantasy = types.InlineKeyboardButton(text=SETTING_FANTASY,
                                                callback_data=SETTING_FANTASY)
    button_sci_fi = types.InlineKeyboardButton(text=SETTING_SCI_FI,
                                               callback_data=SETTING_SCI_FI)
    button_horror = types.InlineKeyboardButton(text=SETTING_HORROR,
                                               callback_data=SETTING_HORROR)
    button_mystery = types.InlineKeyboardButton(text=SETTING_MYSTERY,
                                                callback_data=SETTING_MYSTERY)
    keyboard.add(button_fantasy, button_sci_fi, button_horror, button_mystery)
    # Отправляем сообщение с клавиатурой и просим пользователя выбрать сеттинг 
    data["step"] = STEP_SETTING
    bot.send_message(message.chat.id,
                     "Выбери один из предложенных сеттингов или напиши свой вариант.",
                     reply_markup=keyboard)

# Определяем обработчик всех текстовых сообщений 
@bot.message_handler(content_types=["text"])
def text(message):
    # Проверяем, есть ли данные пользователя в словаре 
    if message.chat.id in user_data:
        # Получаем данные пользователя из словаря 
        # Проверяем, какой шаг ожидает бот от пользователя 
        if data["step"] == STEP_SETTING:
            # Сохраняем ответ пользователя в поле setting 
            data["setting"] = message.text 
            # Выводим ответ пользователя в консоль (можно удалить эту строку) 
            print(data["setting"]) 
            # Переходим к следующему шагу - описанию персонажа 
            data["step"] == STEP_CHARACTER

        elif data["step"] == "character":
            # Сохраняем ответ пользователя в поле character 
            data["character"] = message.text 
            user_data[message.from_user.id] = f"{message.text}"
            # Выводим ответ пользователя в консоль (можно удалить эту строку)  
            print(data["character"])  
            # Переходим к следующему шагу - выбору команды меню  
            menu(message.chat.id) 

        elif data["step"] == "wishes":
             # Сохраняем ответ пользователя в поле wishes   
             data["wishes"] = message.text   
             # Выводим ответ пользователя в консоль (можно удалить эту строку)   
             print(data["wishes"])   
             # Отправляем сообщение пользователю с подтверждением получения всех данных   
             bot.send_message(message.chat.id,
                              f"Спасибо! Я записал все твои пожелания: \nСеттинг: {data['setting']}\nПерсонаж: {data['character']}\nПожелания к сессии: {data['wishes']}") 
             # Сбрасываем данные пользователя из словаря  
             user_data.pop(message.chat.id) 
    else:
        # Если пользователь не ввел команду /start или не ответил на вопросы, то игнорируем его сообщение  
        pass

# Запускаем бота 
bot.polling()