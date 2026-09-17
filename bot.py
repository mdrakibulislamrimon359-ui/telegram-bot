import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Telegram bot is running!")

    def log_message(self, format, *args):
        pass


def start_health_server():
    HTTPServer(("0.0.0.0", PORT), HealthHandler).serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data="help")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    await update.message.reply_text(
        "👋 Welcome!\n\nআমি তোমার Telegram bot। নিচের menu ব্যবহার করো।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Commands:\n\n"
        "/start - Bot শুরু করুন\n"
        "/help - Help দেখুন\n"
        "/about - Bot সম্পর্কে জানুন\n\n"
        "যেকোনো message পাঠালে আমি reply করার চেষ্টা করব।"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ About\n\n"
        "এই bot Python দিয়ে তৈরি এবং Render-এ চালানো যাবে।"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.edit_message_text(
            "📖 Help\n\n"
            "/start - Start\n"
            "/help - Help\n"
            "/about - About\n\n"
            "তুমি আমাকে যেকোনো সাধারণ message পাঠাতে পারো।"
        )
    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ About\n\n"
            "তোমার Telegram bot সফলভাবে চালু আছে।"
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    replies = {
        "hi": "হ্যালো! 👋",
        "hello": "হ্যালো! 👋",
        "হাই": "হ্যালো! 👋",
        "হ্যালো": "হ্যালো! 👋",
        "help": "Help দেখতে /help লিখুন।",
    }

    reply = replies.get(text.lower())
    if reply:
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text(
            f"তুমি লিখেছো: {text}\n\n"
            "আমি তোমার message পেয়েছি। 😊\n"
            "/help লিখলে available commands দেখতে পারবে।"
        )


def main():
    threading.Thread(target=start_health_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
