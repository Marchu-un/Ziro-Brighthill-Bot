# Импортируем модуль для работы с телеграм-ботом
import config
# Импортируем модуль для работы с телеграм-ботом
import telebot
# Импортируем модуль для создания объектов ForceReply
from telebot import types

# Создаем объект бота с помощью токена, полученного от @BotFather
bot = telebot.TeleBot(config.tg_token)

# Создаем словарь для хранения состояния пользователя
user_state = {}

# Определяем константы для разных состояний
STATE_START = 0  # начальное состояние
STATE_GAME_WORLD = 1  # состояние после первого вопроса
STATE_CHARACTER = 2  # состояние после второго вопроса
STATE_WISHES = 3  # состояние после третьего вопроса

game_world, character, wishes = "", "", ""


# Определяем обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):

    # Отправляем приветственное сообщение пользователю
    bot.send_message(message.chat.id, "Привет! Опиши свои пожелания по игровому миру")
    # Создаем объект ForceReply для ожидания ответа от пользователя
    reply = types.ForceReply(selective=False)
    # Отправляем сообщение с ForceReply 
    bot.send_message(message.chat.id, "Напиши свой ответ", reply_markup=reply,
                     reply_to_message_id=message.message_id)
    # Устанавливаем состояние пользователя на STATE_GAME_WORLD 
    user_state[message.chat.id] = STATE_GAME_WORLD


# Определяем обработчик всех текстовых сообщений
@bot.message_handler(content_types=["text"])
def text(message):
    global game_world
    global character
    global wishes
    # Получаем текущее состояние пользователя 
    state = user_state.get(message.chat.id, STATE_START)

    # В зависимости от состояния выполняем разные действия 
    if state == STATE_GAME_WORLD:
        # Сохраняем ответ пользователя в переменную game_world 
        game_world = message.text
        # Выводим ответ пользователя в консоль (можно удалить эту строку) 
        print(game_world)
        # Создаем объект ForceReply для ожидания ответа от пользователя 
        reply = types.ForceReply(selective=False)
        # Отправляем сообщение с ForceReply  
        bot.send_message(message.chat.id, "Теперь опиши своих персонажей!", reply_markup=reply,
                         reply_to_message_id=message.message_id)
        # Устанавливаем состояние пользователя на STATE_CHARACTER  
        user_state[message.chat.id] = STATE_CHARACTER

    elif state == STATE_CHARACTER:
        # Сохраняем ответ пользователя в переменную character
        character = message.text
        # Выводим ответ пользователя в консоль (можно удалить эту строку)
        print(character)
        # Создаем объект ForceReply для ожидания ответа от пользователя
        reply = types.ForceReply(selective=False)
        # Отправляем сообщение с ForceReply
        bot.send_message(message.chat.id, "А теперь опиши общие пожелания к сессии!", reply_markup=reply,
                         reply_to_message_id=message.message_id)
        # Устанавливаем состояние пользователя на STATE_WISHES
        user_state[message.chat.id] = STATE_WISHES

    elif state == STATE_WISHES:
        # Определяем обработчик для получения ответа на третий вопрос 
        # Сохраняем ответ пользователя в переменную wishes 
        wishes = message.text
        # Выводим ответ пользователя в консоль (можно удалить эту строку) 
        print(wishes)
        # Отправляем сообщение пользователю с подтверждением получения всех данных 
        bot.send_message(message.chat.id,
                         f"Спасибо! Я записал все твои пожелания: \nИгровой мир: {game_world}\nПерсонажи: {character}\nПожелания к сессии: {wishes}")


# Запускаем бота
bot.polling()
