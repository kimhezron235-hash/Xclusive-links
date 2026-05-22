import telebot
import os
from flask import Flask, request

BOT_TOKEN = os.environ.get("8715495543:AAEm1sbj7e726KdjwpW7-Yci34obU9LohYQ")
CHANNEL_ID = os.environ.get("-1001331429198")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Submit Link", callback_data="submit"))
    markup.add(telebot.types.InlineKeyboardButton("Help", callback_data="help"))
    bot.send_message(message.chat.id,
        "Welcome to Xclusive Link Exchange Bot!\n\nClick 'Submit Link' to share your link instantly.",
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "submit")
def submit_link(call):
    msg = bot.send_message(call.message.chat.id, "Send me the link:")
    bot.register_next_step_handler(msg, post_link)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_handler(call):
    bot.send_message(call.message.chat.id, "Send a link and it posts immediately. Use /start to begin.")

def post_link(message):
    link = message.text.strip()
    if not link.startswith("http"):
        bot.send_message(message.chat.id, "❌ Invalid link. Please send a proper URL.")
        return
    bot.send_message(CHANNEL_ID, f"🔗 {link}\n\nShared via Xclusive Link Exchange")
    bot.send_message(message.chat.id, "✅ Posted to channel!")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return 'Bot is running', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RAILWAY_STATIC_URL')}/{BOT_TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))