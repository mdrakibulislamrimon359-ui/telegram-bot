import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from openai import AsyncOpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ==========================================
# RJ TEAM BOT SETTINGS
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
PORT = int(os.getenv("PORT", "10000"))

COMMUNITY_NAME = "RJ Team Bangladesh Community"
CREATOR_NAME = "Rakib Sar"

OWNER_USERNAME = "@RJteam1"
PARTNER_USERNAME = "@Apple20237"
ASSISTANT_USERNAME = "@Apple20237"

TIKTOK_USERNAME = "lyrics.song333"
YOUTUBE_LINK = "https://youtube.com/@rakib22"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# ==========================================
# RENDER HEALTH SERVER
# ==========================================

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


# ==========================================
# TRANSLATE BUTTON
# ==========================================

def translate_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🌐 Translate",
                callback_data="translate"
            )
        ]
    ])


def language_keyboard():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="lang_English"
            ),
            InlineKeyboardButton(
                "🇮🇳 Hindi",
                callback_data="lang_Hindi"
            ),
        ],

        [
            InlineKeyboardButton(
                "🇸🇦 Arabic",
                callback_data="lang_Arabic"
            ),
            InlineKeyboardButton(
                "🇵🇰 Urdu",
                callback_data="lang_Urdu"
            ),
        ],

        [
            InlineKeyboardButton(
                "🇨🇳 Chinese",
                callback_data="lang_Chinese"
            ),
            InlineKeyboardButton(
                "🇯🇵 Japanese",
                callback_data="lang_Japanese"
            ),
        ],

        [
            InlineKeyboardButton(
                "🇰🇷 Korean",
                callback_data="lang_Korean"
            ),
            InlineKeyboardButton(
                "🇧🇩 Bangla",
                callback_data="lang_Bangla"
            ),
        ],

        [
            InlineKeyboardButton(
                "🇫🇷 French",
                callback_data="lang_French"
            ),
            InlineKeyboardButton(
                "🇩🇪 German",
                callback_data="lang_German"
            ),
        ],

        [
            InlineKeyboardButton(
                "🇪🇸 Spanish",
                callback_data="lang_Spanish"
            ),
            InlineKeyboardButton(
                "🇹🇷 Turkish",
                callback_data="lang_Turkish"
            ),
        ],

        [
            InlineKeyboardButton(
                "❌ Close",
                callback_data="close_translate"
            )
        ]
    ])


# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "👋 আসসালামু আলাইকুম! 🌸\n\n"

        "🤖 আমি **RJ Team Bot**\n\n"

        "💬 আপনি আমাকে যেকোনো প্রশ্ন করতে পারেন।\n"
        "🇧🇩 আমি সাধারণভাবে বাংলায় উত্তর দেব।\n\n"

        "✨ প্রশ্নের বিষয় অনুযায়ী সুন্দর ও উপযুক্ত Emoji ব্যবহার করব।\n\n"

        "🌐 প্রতিটি AI উত্তরের নিচে **Translate** বাটন থাকবে।\n\n"

        "🚀 শুরু করতে আপনার প্রশ্ন লিখে Send করুন।"
    )


# ==========================================
# HELP
# ==========================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🤖 **RJ Team Bot Help**\n\n"

        "💬 যেকোনো প্রশ্ন সরাসরি লিখুন\n"
        "🇧🇩 উত্তর সাধারণভাবে বাংলায় পাবেন\n"
        "✨ প্রশ্ন অনুযায়ী সুন্দর Emoji থাকবে\n"
        "🌐 Translate দিয়ে বিভিন্ন ভাষায় অনুবাদ করতে পারবেন\n\n"

        "📌 Commands:\n\n"

        "▶️ /start — Bot চালু\n"
        "▶️ /help — Help\n"
        "▶️ /about — Bot সম্পর্কে\n"
        "▶️ /owners — Team Information\n"
        "▶️ /reset — Conversation memory reset"
    )


# ==========================================
# ABOUT
# ==========================================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🤖 **RJ Team Bot**\n\n"

        f"🏠 Community: {COMMUNITY_NAME}\n"
        f"👤 Creator: {CREATOR_NAME}\n\n"

        "👑 Owner: @RJteam1\n"
        "🤝 Partner: @Apple20237\n"
        "🛠️ Assistant: @Apple20237\n\n"

        "🎵 TikTok: lyrics.song333\n"
        "▶️ YouTube: https://youtube.com/@rakib22\n\n"

        "🇧🇩 RJ Team Bangladesh Community\n"
        "✨ Smart • Friendly • Helpful"
    )


# ==========================================
# OWNERS / TEAM INFORMATION
# ==========================================

async def owners(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "👑 Owner",
                url="https://t.me/RJteam1"
            )
        ],

        [
            InlineKeyboardButton(
                "🤝 Partner",
                url="https://t.me/Apple20237"
            )
        ],

        [
            InlineKeyboardButton(
                "🛠️ Assistant",
                url="https://t.me/Apple20237"
            )
        ],

        [
            InlineKeyboardButton(
                "▶️ YouTube",
                url=YOUTUBE_LINK
            )
        ]
    ])

    await update.message.reply_text(

        "👑 **RJ Team Team Information**\n\n"

        f"👑 **Owner:** {OWNER_USERNAME}\n"
        f"🤝 **Partner:** {PARTNER_USERNAME}\n"
        f"🛠️ **Assistant:** {ASSISTANT_USERNAME}\n\n"

        f"🎵 **Owner TikTok:** {TIKTOK_USERNAME}\n"
        f"▶️ **Owner YouTube:** {YOUTUBE_LINK}\n\n"

        f"🤖 **Created by:** {COMMUNITY_NAME}\n"
        f"👤 **Creator:** {CREATOR_NAME}\n\n"

        "✨ RJ Team-এর পক্ষ থেকে আপনাকে স্বাগতম! 🇧🇩",

        reply_markup=keyboard
    )


# ==========================================
# RESET
# ==========================================

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["history"] = []

    await update.message.reply_text(

        "🧹 Conversation memory reset করা হয়েছে।\n\n"
        "✨ এখন নতুন করে কথা বলতে পারেন।"
    )


# ==========================================
# CREATOR QUESTION
# ==========================================

def is_creator_question(text):

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
        "creator কে"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


def creator_answer():

    return (

        "🤖 আমাকে তৈরি করেছে **RJ Team Bangladesh Community** 🇧🇩\n\n"

        "👤 **Creator:** Rakib Sar\n"
        "👑 **Owner:** @RJteam1\n"
        "🤝 **Partner:** @Apple20237\n"
        "🛠️ **Assistant:** @Apple20237\n\n"

        "🎵 **TikTok:** lyrics.song333\n"
        "▶️ **YouTube:** https://youtube.com/@rakib22\n\n"

        "✨ আমি RJ Team-এর AI Assistant।"
    )


# ==========================================
# AI RESPONSE
# ==========================================

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if not update.message.text:
        return

    user_text = update.message.text.strip()

    if not user_text:
        return


    # Creator question
    if is_creator_question(user_text):

        answer = creator_answer()

        sent = await update.message.reply_text(
            answer,
            reply_markup=translate_keyboard()
        )

        context.user_data["last_answer"] = answer
        context.user_data["last_message_id"] = sent.message_id

        return


    # Conversation history
    history = context.user_data.setdefault(
        "history",
        []
    )

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

                "You are RJ Team Bot, a helpful, friendly and smart "
                "Telegram AI assistant. "

                "IMPORTANT LANGUAGE RULE: "
                "Always answer in natural Bangla/Bengali by default, "
                "even when the user asks in English or Banglish. "

                "Only use another language when the user explicitly "
                "requests another language. "

                "Make answers easy to understand and useful. "

                "Use beautiful and relevant emojis according to "
                "the topic and mood of the user's message. "

                "For example: "
                "education can use 📚🎓✍️, "
                "technology can use 💻🤖⚙️, "
                "business can use 💰📈💼, "
                "love or feelings can use ❤️🥰🌹, "
                "success can use 🎉🏆✨, "
                "warning can use ⚠️🚨, "
                "general useful information can use 💡✅. "

                "Do NOT use too many emojis. "
                "Do NOT put random emojis everywhere. "
                "Use emojis naturally to make the answer "
                "beautiful and friendly. "

                "Use short paragraphs, headings and bullet points "
                "when they improve readability. "

                "Be accurate, helpful, friendly and concise. "

                "If asked who created, made, built or owns this bot, "
                "give the following information: "

                "Created by RJ Team Bangladesh Community. "
                "Creator: Rakib Sar. "
                "Owner: @RJteam1. "
                "Partner: @Apple20237. "
                "Assistant: @Apple20237. "
                "TikTok: lyrics.song333. "
                "YouTube: https://youtube.com/@rakib22. "

                "Do not describe anyone as the owner unless "
                "the user specifically asks for the owner. "
                "When giving general creator information, "
                "say Creator: Rakib Sar and Created by: "
                "RJ Team Bangladesh Community."
            ),

            input=history
        )


        answer = response.output_text.strip()


        if not answer:

            answer = (
                "😔 দুঃখিত, এখন কোনো উত্তর পাওয়া যায়নি।"
            )


        history.append({

            "role": "assistant",
            "content": answer

        })


        context.user_data["last_answer"] = answer


        # Telegram message limit
        for i in range(
            0,
            len(answer),
            4000
        ):

            chunk = answer[i:i + 4000]

            sent = await update.message.reply_text(

                chunk,

                reply_markup=translate_keyboard()
            )

            context.user_data[
                "last_message_id"
            ] = sent.message_id


    except Exception as e:

        print(
            "AI ERROR:",
            repr(e)
        )

        await update.message.reply_text(

            "❌ দুঃখিত, AI উত্তর দিতে সমস্যা হচ্ছে।\n"
            "⏳ একটু পরে আবার চেষ্টা করুন।"
        )


# ==========================================
# TRANSLATE MENU
# ==========================================

async def translate_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(

        "🌐 **কোন ভাষায় Translate করতে চান?**\n\n"
        "👇 আপনার পছন্দের ভাষায় চাপ দিন।",

        reply_markup=language_keyboard()
    )


# ==========================================
# TRANSLATE
# ==========================================

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    language = query.data.replace(
        "lang_",
        ""
    )

    answer = context.user_data.get(
        "last_answer"
    )


    if not answer:

        await query.message.reply_text(

            "❌ Translate করার মতো কোনো "
            "সাম্প্রতিক উত্তর পাওয়া যায়নি।"
        )

        return


    try:

        response = await client.responses.create(

            model=OPENAI_MODEL,

            instructions=(

                f"Translate the following text accurately "
                f"into {language}. "

                "Keep the original meaning and important details. "

                "Do not add extra information. "

                "Make the translation natural and easy to understand."
            ),

            input=answer
        )


        translated = response.output_text.strip()


        if not translated:

            translated = (
                "❌ Translation পাওয়া যায়নি।"
            )


        await query.message.reply_text(

            f"🌐 **{language} Translation**\n\n"
            f"{translated}"
        )


    except Exception as e:

        print(
            "TRANSLATE ERROR:",
            repr(e)
        )

        await query.message.reply_text(

            "❌ Translation করতে সমস্যা হয়েছে।\n"
            "⏳ একটু পরে আবার চেষ্টা করুন।"
        )


# ==========================================
# CLOSE TRANSLATE
# ==========================================

async def close_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    try:

        await query.message.delete()

    except Exception:

        await query.message.edit_text(
            "❌ Translate menu বন্ধ করা হয়েছে।"
        )


# ==========================================
# MAIN
# ==========================================

async def main():

    Thread(
        target=start_health_server,
        daemon=True
    ).start()


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )


    # Commands
    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("about", about)
    )

    app.add_handler(
        CommandHandler("owners", owners)
    )

    app.add_handler(
        CommandHandler("reset", reset)
    )


    # Translate
    app.add_handler(
        CallbackQueryHandler(
            translate_button,
            pattern="^translate$"
        )
    )


    # Language
    app.add_handler(
        CallbackQueryHandler(
            translate_text,
            pattern="^lang_"
        )
    )


    # Close
    app.add_handler(
        CallbackQueryHandler(
            close_translate,
            pattern="^close_translate$"
        )
    )


    # Normal messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_reply
        )
    )


    print(
        "RJ Team Bot is running..."
    )


    await app.initialize()

    await app.start()

    await app.updater.start_polling()


    try:

        await asyncio.Event().wait()

    finally:

        await app.updater.stop()
        await app.stop()
        await app.shutdown()


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    asyncio.run(main())