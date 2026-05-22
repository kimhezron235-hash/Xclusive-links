import telebot
from telebot import types
import os

BOT_TOKEN = "8715495543:AAEm1sbj7e726KdjwpW7-Yci34obU9LohYQ"
CHANNEL_ID = "-1001331429198"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📤 Submit Link", callback_data="submit"))
    bot.send_message(message.chat.id,
        "👋 Welcome to Xclusive Link Exchange!\n\nTap below to share your link instantly to the channel.",
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "submit")
def ask_link(call):
    msg = bot.send_message(call.message.chat.id, "🔗 Send your link now:")
    bot.register_next_step_handler(msg, post_link)

def post_link(message):
    link = message.text.strip()
    if not link.startswith("http"):
        bot.send_message(message.chat.id, "❌ Invalid link. Please send a valid URL starting with http.")
        return
    bot.send_message(CHANNEL_ID, f"🔗 {link}")
    bot.send_message(message.chat.id, "✅ Your link has been posted!")

bot.polling(non_stop=True)