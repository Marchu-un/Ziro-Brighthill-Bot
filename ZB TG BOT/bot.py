import telebot
import config

bot = telebot.TeleBot(config.token)

# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, 'Привет, я бот. Как дела?')

# обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def echo_handler(message):
    bot.reply_to(message, message.text)

# запускаем бота
if __name__ == '__main__':
    bot.infinity_polling()