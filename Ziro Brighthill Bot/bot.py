import openai
import telebot
import logging
import os
import time
import config

openai.api_key = config.gpt_token
bot = telebot.TeleBot(config.tg_token)

# Logging
if not os.path.exists('/tmp/bot_log/'):
    os.makedirs('/tmp/bot_log/')

logging.basicConfig(filename='/tmp/bot_log/log.txt', level=logging.ERROR,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет!\nЯ ChatGPT Telegram Bot\U0001F916\nЗадай мне любой вопрос и я постараюсь на него ответиь')

def generate_response(prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        return response["choices"][0]["text"]

@bot.message_handler(commands=['bot'])
def command_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.reply_to(message, text=response)

@bot.message_handler(func = lambda _: True)
def handle_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.send_message(chat_id=message.from_user.id, text=response)
    
print('ChatGPT Bot is working')

while True:
    try:
        bot.polling()
    except (telebot.apihelper.ApiException, ConnectionError) as e:
        logging.error(str(e))
        time.sleep(5)
        continue