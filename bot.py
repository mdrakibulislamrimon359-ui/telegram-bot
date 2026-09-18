import os
import asyncio
import logging
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

from openai import AsyncOpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna").strip()
PORT = int(os.getenv("PORT", "10000"))

OWNER = "@RJteam1"
PARTNER = "@Apple20237"
ASSISTANT = "@Apple20237"
TIKTOK = "lyrics.song333"
YOUTUBE = "https://youtube.com/@rakib22"

BOT_NAME = "RJ Team AI Community Bangladesh 🇧🇩"

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("RJ_TEAM_AI")

# =========================================================
# ENV CHECK
# =========================================================

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN পাওয়া যায়নি। Render Environment Variables চেক করুন।")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY পাওয়া যায়নি। Render Environment Variables চেক করুন।"
    )

# =========================================================
# OPENAI CLIENT
# =========================================================

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# =========================================================
# USER MEMORY
# =========================================================

user_history = {}

MAX_HISTORY = 12

# =========================================================
# AI SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
তুমি RJ Team AI Community Bangladesh-এর official AI assistant।

তোমার কাজ:
- ব্যবহারকারীর প্রশ্নের সঠিক ও সহজ উত্তর দেওয়া।
- ব্যবহারকারী বাংলা লিখলে বাংলায় উত্তর দেওয়া।
- Banglish লিখলে সহজ বাংলা/Banglish-এ উত্তর দেওয়া।
- English প্রশ্ন হলে English-এ উত্তর দেওয়া।
- প্রয়োজন হলে উদাহরণ দিয়ে বোঝানো।
- Programming, Telegram Bot, AI, OpenAI, Technology, Translation ইত্যাদিতে সাহায্য করা।
- উত্তর সংক্ষিপ্ত, পরিষ্কার এবং বন্ধুত্বপূর্ণ রাখা।
- নিজের সম্পর্কে মিথ্যা দাবি করা যাবে না।
- তুমি RJ Team AI Community Bangladesh-এর AI Assistant।
- কেউ Owner সম্পর্কে জিজ্ঞেস করলে Owner হিসেবে @RJteam1 বলবে।
- Partner/Assistant হিসেবে @Apple20237 বলবে।
"""

# =========================================================
# HEALTH SERVER FOR RENDER
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"RJ Team AI Community Bangladesh is running successfully."
        )

    def log_message(self, format, *args):
        return


def run_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    logger.info(f"Health server running on port {PORT}")
    server.serve_forever()


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("👑 Owners", callback_data="owners"),
        ],
        [
            InlineKeyboardButton("🌐 Translate", callback_data="translate"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"🤖 <b>{BOT_NAME}</b>\n\n"
        "স্বাগতম! 🇧🇩\n\n"
        "আমি আপনার AI Assistant।\n"
        "💡 AI • Technology • Tools • Translation\n\n"
        "আপনার প্রশ্ন লিখে পাঠান। 🚀\n\n"
        "👑 Owner: @RJteam1"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup,
    )


# =========================================================
# HELP
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "❓ <b>RJ Team AI Bot Help</b>\n\n"
        "💬 যেকোনো প্রশ্ন সরাসরি লিখে পাঠান।\n\n"
        "📌 Commands:\n"
        "/start - 🚀 Bot চালু করুন\n"
        "/help - ❓ Help দেখুন\n"
        "/about - ℹ️ Bot সম্পর্কে\n"
        "/owners - 👑 Owner & Team\n"
        "/reset - 🔄 AI memory reset\n\n"
        "🌐 Translation-এর জন্য Translate button ব্যবহার করুন।"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


# =========================================================
# ABOUT
# =========================================================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🤖 <b>RJ Team AI Community Bangladesh</b>\n\n"
        "🇧🇩 বাংলাদেশের AI ও Technology Community\n\n"
        "💡 AI • Technology • Tools • Translation\n"
        "🚀 Learn • Create • Share • Connect\n\n"
        "👑 Powered by RJ Team"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


# =========================================================
# OWNERS
# =========================================================

async def owners(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👑 <b>RJ Team Information</b>\n\n"
        f"👑 Owner: {OWNER}\n"
        f"🤝 Partner: {PARTNER}\n"
        f"🧑‍💻 Assistant: {ASSISTANT}\n\n"
        f"🎵 TikTok: {TIKTOK}\n"
        f"▶️ YouTube: {YOUTUBE}\n\n"
        "🇧🇩 RJ Team AI Community Bangladesh"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


# =========================================================
# RESET
# =========================================================

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    user_history.pop(user_id, None)

    await update.message.reply_text(
        "🔄 আপনার AI conversation memory reset করা হয়েছে।\n\n"
        "এখন নতুন conversation শুরু করতে পারেন। ✅"
    )


# =========================================================
# AI RESPONSE
# =========================================================

async def ai_reply(user_id: int, user_text: str):

    if user_id not in user_history:
        user_history[user_id] = []

    history = user_history[user_id]

    # Add user message
    history.append(
        {
            "role": "user",
            "content": user_text,
        }
    )

    # Keep only recent messages
    history = history[-MAX_HISTORY:]

    try:

        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=history,
        )

        answer = getattr(response, "output_text", None)

        if not answer:
            answer = "দুঃখিত, এই মুহূর্তে কোনো উত্তর পাওয়া যায়নি।"

        answer = answer.strip()

        # Save assistant answer
        history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        user_history[user_id] = history[-MAX_HISTORY:]

        return answer

    except Exception as e:

        logger.exception("OPENAI ERROR")

        # Remove failed user message
        if history and history[-1].get("role") == "user":
            history.pop()

        # Give useful error for debugging
        error_message = str(e)

        return (
            "❌ AI উত্তর দিতে সমস্যা হচ্ছে।\n\n"
            "🔧 OpenAI Error:\n"
            f"{error_message[:1200]}\n\n"
            "⚠️ Render-এর OPENAI_API_KEY এবং OPENAI_MODEL চেক করুন।"
        )


# =========================================================
# TEXT MESSAGE
# =========================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    user_text = update.message.text.strip()

    if not user_text:
        return

    # Typing indicator
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
    except Exception:
        pass

    answer = await ai_reply(
        user_id=user_id,
        user_text=user_text,
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🌐 Translate",
                callback_data="translate",
            ),
            InlineKeyboardButton(
                "🔄 Reset",
                callback_data="reset",
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        answer,
        reply_markup=reply_markup,
    )


# =========================================================
# CALLBACK BUTTONS
# =========================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    if query.data == "about":

        text = (
            "🤖 <b>RJ Team AI Community Bangladesh</b>\n\n"
            "🇧🇩 বাংলাদেশের AI ও Technology Community\n"
            "💡 AI • Technology • Tools • Translation\n"
            "🚀 Learn • Create • Share • Connect"
        )

        await query.message.reply_text(
            text,
            parse_mode="HTML",
        )

    elif query.data == "owners":

        text = (
            "👑 <b>RJ Team</b>\n\n"
            f"Owner: {OWNER}\n"
            f"Partner: {PARTNER}\n"
            f"Assistant: {ASSISTANT}\n\n"
            f"🎵 TikTok: {TIKTOK}\n"
            f"▶️ YouTube: {YOUTUBE}"
        )

        await query.message.reply_text(
            text,
            parse_mode="HTML",
        )

    elif query.data == "help":

        text = (
            "❓ <b>Help</b>\n\n"
            "/start - Bot চালু\n"
            "/help - Help\n"
            "/about - About\n"
            "/owners - Team information\n"
            "/reset - AI memory reset\n\n"
            "💬 প্রশ্ন লিখে পাঠান।"
        )

        await query.message.reply_text(
            text,
            parse_mode="HTML",
        )

    elif query.data == "reset":

        user_history.pop(user_id, None)

        await query.message.reply_text(
            "🔄 আপনার AI memory reset হয়েছে।"
        )

    elif query.data == "translate":

        await query.message.reply_text(
            "🌐 Translation:\n\n"
            "যে text translate করতে চান, সেটি পাঠান।\n\n"
            "উদাহরণ:\n"
            "Translate this into Bangla: Hello Bangladesh 🇧🇩"
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception(
        "Telegram error:",
        exc_info=context.error,
    )


# =========================================================
# MAIN
# =========================================================

def main():

    logger.info("Starting RJ Team AI Community Bangladesh Bot...")
    logger.info(f"Model: {OPENAI_MODEL}")

    # Render health server
    health_thread = Thread(
        target=run_health_server,
        daemon=True,
    )

    health_thread.start()

    # Telegram application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("about", about)
    )

    application.add_handler(
        CommandHandler("owners", owners)
    )

    application.add_handler(
        CommandHandler("reset", reset)
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    # Error handler
    application.add_error_handler(error_handler)

    logger.info("Bot is running...")

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()