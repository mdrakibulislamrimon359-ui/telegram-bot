import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
PORT = int(os.getenv("PORT", "10000"))

# RJ Team Information
COMMUNITY_NAME = "RJ Team Bangladesh Community"
CREATOR_NAME = "Rakib Sar"
OWNER_USERNAME = "@RJteam1"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"RJ Team Bot is running!")

    def log_message(self, format, *args):
        pass


def start_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalamu Alaikum!\n\n"
        "আমি RJ Team Bot 🤖\n"
        "আপনি যেকোনো প্রশ্ন করতে পারেন।\n\n"
        "💡 শুধু আপনার প্রশ্ন লিখে Send করুন।"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 RJ Team Bot Help\n\n"
        "• যেকোনো প্রশ্ন সরাসরি লিখুন\n"
        "• /start — Bot চালু\n"
        "• /help — Help\n"
        "• /about — Bot সম্পর্কে\n"
        "• /owners — Creator ও Owner তথ্য\n"
        "• /reset — Memory reset"
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 RJ Team Bot\n\n"
        f"🏠 Community: {COMMUNITY_NAME}\n"
        f"👤 Creator: {CREATOR_NAME}\n"
        f"👑 Owner: {OWNER_USERNAME}\n\n"
        "AI-powered Telegram assistant."
    )


async def owners(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 RJ Team Bot Information\n\n"
        f"🏠 Community: {COMMUNITY_NAME}\n"
        f"👤 Creator: {CREATOR_NAME}\n"
        f"👑 Owner: {OWNER_USERNAME}"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history"] = []
    await update.message.reply_text(
        "✅ আপনার conversation memory reset করা হয়েছে।"
    )


def is_creator_question(text: str) -> bool:
    text = text.lower().strip()

    keywords = [
        "আপনাকে কে বানিয়েছে",
        "কে বানিয়েছে",
        "কে তৈরি করেছে",
        "কে তোমাকে বানিয়েছে",
        "কে তোমাকে তৈরি করেছে",
        "তোমাকে কে বানিয়েছে",
        "তোমাকে কে তৈরি করেছে",
        "who made you",
        "who created you",
        "who built you",
        "who is your creator",
        "who created this bot",
        "bot কে বানিয়েছে",
        "bot কে তৈরি করেছে",
        "creator কে",
    ]

    return any(keyword in text for keyword in keywords)


def creator_answer() -> str:
    return (
        "🤖 আমাকে তৈরি করেছে RJ Team Bangladesh Community\n"
        "👤 Creator: Rakib Sar\n"
        "👑 Owner: @RJteam1"
    )


async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()

    if not user_text:
        return

    # Creator/Owner প্রশ্নের নির্দিষ্ট উত্তর
    if is_creator_question(user_text):
        await update.message.reply_text(creator_answer())
        return

    history = context.user_data.setdefault("history", [])

    history.append({
        "role": "user",
        "content": user_text
    })

    if len(history) > 20:
        history[:] = history[-20:]

    try:
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=(
                "You are RJ Team Bot, a helpful and friendly Telegram AI assistant. "
                "Answer clearly and accurately. "
                "The user may write Bangla, Banglish, or English. "
                "Reply in the same language when practical. "
                "Be concise but helpful. "
                "If asked who created, made, built, or owns this bot, "
                "say it was created by RJ Team Bangladesh Community, "
                "the creator is Rakib Sar, and the owner is @RJteam1."
            ),
            input=history,
        )

        answer = response.output_text.strip()

        if not answer:
            answer = "দুঃখিত, এখন কোনো উত্তর পাওয়া যায়নি।"

        history.append({
            "role": "assistant",
            "content": answer
        })

        for i in range(0, len(answer), 4000):
            await update.message.reply_text(answer[i:i + 4000])

    except Exception as e:
        print("AI ERROR:", repr(e))
        await update.message.reply_text(
            "❌ AI উত্তর দিতে সমস্যা হচ্ছে। একটু পরে আবার চেষ্টা করুন।"
        )


async def main():
    Thread(target=start_health_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("owners", owners))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("RJ Team Bot is running...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())