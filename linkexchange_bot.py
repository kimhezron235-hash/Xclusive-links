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
    msg = bot.send_message(call.message.chat.id, 
        "📎 Send your post now:\n\n• Text link only, OR\n• Photo with caption containing your link")
    bot.register_next_step_handler(msg, post_link)

def post_link(message):
    try:
        # Photo with caption
        if message.photo:
            caption = message.caption or ""
            bot.send_photo(CHANNEL_ID, 
                message.photo[-1].file_id, 
                caption=caption)
            bot.send_message(message.chat.id, "✅ Your post has been shared to the channel!")

        # Video with caption
        elif message.video:
            caption = message.caption or ""
            bot.send_video(CHANNEL_ID,
                message.video.file_id,
                caption=caption)
            bot.send_message(message.chat.id, "✅ Your post has been shared to the channel!")

        # Text link
        elif message.text:
            link = message.text.strip()
            if not link.startswith("http"):
                bot.send_message(message.chat.id, "❌ Invalid link. Must start with http")
                msg = bot.send_message(message.chat.id, "🔗 Try again:")
                bot.register_next_step_handler(msg, post_link)
                return
            bot.send_message(CHANNEL_ID, f"🔗 {link}")
            bot.send_message(message.chat.id, "✅ Your link has been posted to the channel!")

        else:
            bot.send_message(message.chat.id, "❌ Unsupported format. Send a link, photo, or video.")
            msg = bot.send_message(message.chat.id, "🔗 Try again:")
            bot.register_next_step_handler(msg, post_link)

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Failed to post. Make sure the bot is admin in the channel.")

bot.polling(non_stop=True)