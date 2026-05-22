import telebot
from telebot import types
import os

BOT_TOKEN = "8715495543:8715495543:AAHRA8axUsMf0XRRZKCfFE_X0rtLUgZEQ-8"
ADMIN_IDS = [1098654847]
CHANNEL_ID = "-100133142919"  # note the minus sign for channels

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Submit Link", callback_data="submit"))
    markup.add(types.InlineKeyboardButton("Help", callback_data="help"))
    bot.send_message(message.chat.id,
        "Welcome to Xclusive Link Exchange Bot!\n\nClick 'Submit Link' to share your link instantly.",
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "submit")
def submit_link(call):
    msg = bot.send_message(call.message.chat.id, "Send me the link you want to share:")
    bot.register_next_step_handler(msg, post_link)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_handler(call):
    bot.send_message(call.message.chat.id,
        "Send a link and it will be posted to the channel immediately.\n\nUse /start to begin.")

def post_link(message):
    link = message.text.strip()
    if not link.startswith("http"):
        bot.send_message(message.chat.id, "❌ That doesn't look like a valid link. Please send a proper URL.")
        return
    try:
        bot.send_message(CHANNEL_ID, f"🔗 {link}\n\nShared via Xclusive Link Exchange")
        bot.send_message(message.chat.id, "✅ Your link has been posted to the channel!")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Failed to post. Please try again.")

bot.polling(non_stop=True)