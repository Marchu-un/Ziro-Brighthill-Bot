import openai
import telebot
import logging
import os
import time
import config
import re # Do we really need it?

openai.api_key = config.gpt_token
bot = telebot.TeleBot(config.tg_token)

# Logging
if not os.path.exists('/tmp/bot_log/'):
    os.makedirs('/tmp/bot_log/')

logging.basicConfig(filename='/tmp/bot_log/log.txt', level=logging.ERROR,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Global variables for storing context and counter
context_dict = {}
counter_dict = {}

Brighthill_initial_prompt = """Я - гейммастер для ДнД игры по имени Зиро Брайтхил.
                             Я провожу игру для одного игрока. Сейчас я начну, опишу сеттинг игры, 
                             предложу User выбрать персонажей и после его ответа открою игру описанием местности в которой он находится"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Get chat_id from message object
    chat_id = message.chat.id
    
    # Get or create context for chat_id
    if chat_id not in context_dict:
        context_dict[chat_id] = Brighthill_initial_prompt

        # Generate prompt with context 
    prompt = f"{context_dict[chat_id]}\nБрайтхилл:"

    response = generate_response(prompt)

    bot.reply_to(message, response)

def generate_response(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [ 
            {"role": "user", "content": prompt} 
            ],
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        return response['choices'][0]['message']['content']

# No context bot response
@bot.message_handler(commands=['bot'])
def command_message(message):
    prompt = message.text
    response = generate_response(prompt)
    bot.reply_to(message, text=response)

# define a regular expression pattern that matches any of the names
name_pattern = r'(Брайтхил|Брайтхилл|брайхилл|брайтхил|Зиро|зиро)'

# define a function that checks if a message matches the condition
def name_or_reply(message):
    # check if the message contains any of the names using re.search
    name_match = re.search(name_pattern, message.text)
    
    # check if the message is a reply to the bot using message.reply_to_message.from_user.is_bot
    if message.reply_to_message is not None:
        reply_match = message.reply_to_message.from_user.is_bot
    else: reply_match = False
    
    # return True if either name_match or reply_match is True, otherwise return False
    return bool(name_match) or bool(reply_match)

@bot.message_handler(func=name_or_reply)
def handle_message(message):
    # Get chat_id from message object
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Append message text to context 
    context_dict[chat_id] += f"{user_id}: {message.text}"
    
    # Get or create counter for chat_id 
    if chat_id not in counter_dict:
        counter_dict[chat_id] = 1
    else:
        counter_dict[chat_id] += 1
    
    # Generate prompt with context 
    prompt = f"{context_dict[chat_id]}\nБрайтхилл:"
    
    # Generate response with ChatGPT 
    response = generate_response(prompt)
    
    # Append response text to context 
    context_dict[chat_id] += f"{response}"
    
    # Add counter to response text 
    response += f"\nMessage #{counter_dict[chat_id]}| User: {user_id} | /reset"
    
     # Send response back to user 
    bot.send_message(chat_id=chat_id , text=response)

@bot.message_handler(commands=['reset'])
def reset_context(message):
     # Get chat_id from message object 
     chat_id = message.from_user.id
     
     # Delete chat_id from both dictionaries 
     del context_dict[chat_id]
     del counter_dict[chat_id]
     
     # Clear prompt variable 
     prompt = ""
     
     # Send confirmation message to user 
     bot.send_message(chat_id=chat_id , text="Conversation reset!")

print('ChatGPT Bot is working')

while True:
   try:
       bot.polling()
   except (telebot.apihelper.ApiException , ConnectionError) as e:
       logging.error(str(e))
       time.sleep(5)
       continue