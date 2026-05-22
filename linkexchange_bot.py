import telebot
from telebot import types
import os
import threading

BOT_TOKEN = "8715495543:AAEm1sbj7e726KdjwpW7-Yci34obU9LohYQ"
CHANNEL_ID = "-1001331429198"

PROMO = """🔥 Free tips in website
🌐 Antoniomartin.netlify.app

⚡ Free Telegram link
👉 t.me/xusivelive

⏳ Link only for first 10 clients, 3 more left."""

bot = telebot.TeleBot(BOT_TOKEN)

def delete_after(chat_id, message_id, delay=300):
    def task():
        import time
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    threading.Thread(target=task, daemon=True).start()

def send_submit_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📤 Submit Link", callback_data="submit"))
    bot.send_message(chat_id,
        "👋 Welcome to Xclusive Link Exchange!\n\nTap below to share your post to the channel.",
        reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    send_submit_menu(message.chat.id)

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'sticker'])
def any_message(message):
    send_submit_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "submit")
def ask_link(call):
    msg = bot.send_message(call.message.chat.id,
        "📎 Send your post now:\n• Text link, OR\n• Photo/video with caption")
    bot.register_next_step_handler(msg, post_link)

def post_link(message):
    try:
        sent = None

        if message.photo:
            caption = message.caption or ""
            sent = bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=caption)

        elif message.video:
            caption = message.caption or ""
            sent = bot.send_video(CHANNEL_ID, message.video.file_id, caption=caption)

        elif message.text:
            link = message.text.strip()
            if not link.startswith("http"):
                bot.send_message(message.chat.id, "❌ Invalid link. Must start with http")
                msg = bot.send_message(message.chat.id, "🔗 Try again:")
                bot.register_next_step_handler(msg, post_link)
                return
            sent = bot.send_message(CHANNEL_ID, f"🔗 {link}")

        else:
            bot.send_message(message.chat.id, "❌ Unsupported format.")
            msg = bot.send_message(message.chat.id, "Try again:")
            bot.register_next_step_handler(msg, post_link)
            return

        if sent:
            delete_after(CHANNEL_ID, sent.message_id, delay=300)
            bot.send_message(message.chat.id,
                f"✅ Posted! Will auto-delete in 5 minutes.\n\n📢 Share our channel too:\n\n{PROMO}")

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Failed to post. Make sure the bot is admin in the channel.")

bot.polling(non_stop=True)