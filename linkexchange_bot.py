import telebot
from telebot import types
import os
import threading
import time

BOT_TOKEN = "8715495543:AAEm1sbj7e726KdjwpW7-Yci34obU9LohYQ"
CHANNEL_ID = "-1001331429198"
PHOTO_URL = "https://raw.githubusercontent.com/kimhezron235-hash/Xclusive-links/main/promo.jpg"

PROMO = """🔥 Free tips in website
🌐 Antoniomartin.netlify.app

⚡ Free Telegram link
👉 t.me/Xclusivelive

⏳ Link only for first 10 clients, 3 more left."""

bot = telebot.TeleBot(BOT_TOKEN)

def delete_after(chat_id, message_id, delay=300):
    def task():
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

@bot.message_handler(func=lambda message: True, content_types=['text','photo','video','document','sticker'])
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
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ I have posted!", callback_data="confirmed"))
            markup.add(types.InlineKeyboardButton("❌ I haven't posted yet", callback_data="not_posted"))
            bot.send_message(message.chat.id,
                "✅ Your link is live!\n\nNow share our promo to YOUR channel, then confirm below:",
                reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Failed to post. Make sure the bot is admin in the channel.")

@bot.callback_query_handler(func=lambda call: call.data == "confirmed")
def confirmed(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, "🙏 Thank you! Here's your promo to share:")
    bot.send_photo(call.message.chat.id, PHOTO_URL, caption=PROMO)

@bot.callback_query_handler(func=lambda call: call.data == "not_posted")
def not_posted(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id,
        "⏰ No problem! Post our link to your channel first, then come back and confirm.\n\nUse /start when ready.")

bot.polling(non_stop=True)