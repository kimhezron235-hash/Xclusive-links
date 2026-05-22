import telebot
from telebot import types
import os

BOT_TOKEN = "8715495543:AAHRA8axUsMf0XRRZKCfFE_X0rtLUgZEQ-8"
ADMIN_IDS = [1098654847] # Replace with your Telegram user ID
CHANNEL_ID = "1001331429198" # Replace with your channel username

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Submit Link", callback_data="submit"))
    markup.add(types.InlineKeyboardButton("Help", callback_data="help"))
    bot.send_message(message.chat.id, 
                     "Welcome to Xclusive Link Exchange Bot!\n\nClick 'Submit Link' to submit your link for review.", 
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "submit")
def submit_link(call):
    msg = bot.send_message(call.message.chat.id, "Send me the link you want to submit:")
    bot.register_next_step_handler(msg, get_link)

def get_link(message):
    user_data[message.chat.id] = {'link': message.text}
    msg = bot.send_message(message.chat.id, "Now send the title/description for the link:")
    bot.register_next_step_handler(msg, get_description)

def get_description(message):
    user_data[message.chat.id]['desc'] = message.text
    link = user_data[message.chat.id]['link']
    desc = user_data[message.chat.id]['desc']
    
    for admin in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Approve", callback_data=f"approve_{message.chat.id}"),
            types.InlineKeyboardButton("Reject", callback_data=f"reject_{message.chat.id}")
        )
        bot.send_message(admin, 
                         f"New link submission:\n\nLink: {link}\nDesc: {desc}\nFrom: {message.from_user.username}", 
                         reply_markup=markup)
    
    bot.send_message(message.chat.id, "Link submitted! You'll be notified once it's reviewed.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve(call):
    user_id = int(call.data.split("_")[1])
    data = user_data.get(user_id)
    if data:
        bot.send_message(CHANNEL_ID, f"{data['desc']}\n{data['link']}")
        bot.send_message(user_id, "Your link was approved and posted!")
        bot.answer_callback_query(call.id, "Approved")
    else:
        bot.answer_callback_query(call.id, "Error: Data not found")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject(call):
    user_id = int(call.data.split("_")[1])
    bot.send_message(user_id, "Your link was rejected.")
    bot.answer_callback_query(call.id, "Rejected")

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_cb(call):
    bot.send_message(call.message.chat.id, "Use this bot to submit links. Admins will review and post approved links to the channel.")

bot.infinity_polling()