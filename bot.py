import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from openai import AsyncOpenAI

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.constants import ChatAction

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
    filters,
)


# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
PORT = int(os.getenv("PORT", "10000"))


# =========================================================
# RJ TEAM INFORMATION
# =========================================================

COMMUNITY_NAME = "RJ Team Bangladesh Community"

CREATOR_NAME = "Rakib Sar"

OWNER_USERNAME = "@RJteam1"
PARTNER_USERNAME = "@Apple20237"
ASSISTANT_USERNAME = "@Apple20237"

TIKTOK_USERNAME = "lyrics.song333"
YOUTUBE_URL = "https://youtube.com/@rakib22"


# =========================================================
# OPENAI
# =========================================================

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)


# =========================================================
# RENDER HEALTH SERVER
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"RJ Team Bot is running!")

    def log_message(self, format, *args):
        return


def start_health_server():

    server = HTTPServer(
        ("0.0.0.0", PORT),
        HealthHandler
    )

    server.serve_forever()


# =========================================================
# TRANSLATE BUTTON
# =========================================================

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
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hi"),
        ],
        [
            InlineKeyboardButton("🇸🇦 Arabic", callback_data="lang_ar"),
            InlineKeyboardButton("🇵🇰 Urdu", callback_data="lang_ur"),
        ],
        [
            InlineKeyboardButton("🇨🇳 Chinese", callback_data="lang_zh"),
            InlineKeyboardButton("🇯🇵 Japanese", callback_data="lang_ja"),
        ],
        [
            InlineKeyboardButton("🇰🇷 Korean", callback_data="lang_ko"),
            InlineKeyboardButton("🇧🇩 Bangla", callback_data="lang_bn"),
        ],
        [
            InlineKeyboardButton("🇫🇷 French", callback_data="lang_fr"),
            InlineKeyboardButton("🇩🇪 German", callback_data="lang_de"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Spanish", callback_data="lang_es"),
            InlineKeyboardButton("🇹🇷 Turkish", callback_data="lang_tr"),
        ],
    ])


LANGUAGES = {
    "lang_en": "English",
    "lang_hi": "Hindi",
    "lang_ar": "Arabic",
    "lang_ur": "Urdu",
    "lang_zh": "Chinese",
    "lang_ja": "Japanese",
    "lang_ko": "Korean",
    "lang_bn": "Bangla",
    "lang_fr": "French",
    "lang_de": "German",
    "lang_es": "Spanish",
    "lang_tr": "Turkish",
}


# =========================================================
# GROUP ISLAMIC NOTICE
# =========================================================

GROUP_NOTICE = """
🕌 ইসলামিক আদব ও গ্রুপ নিয়ম

🚫 গালাগালি, অশালীন ভাষা ও অপমানজনক কথা বলা যাবে না।

🤝 একে অপরের সাথে সম্মানজনক আচরণ করুন।

📚 ভালো ও উপকারী কথা বলুন।

❤️ কাউকে কষ্ট দেওয়া থেকে বিরত থাকুন।

⚠️ প্রথমবার নিয়ম ভঙ্গ করলে সতর্ক করা হবে।
🚨 দ্বিতীয়বার নিয়ম ভঙ্গ করলে গ্রুপ থেকে Kick করা হতে পারে।

🤲 সুন্দর ভাষায় কথা বলুন এবং সবাইকে সম্মান করুন।
"""


# =========================================================
# BAD WORDS
# =========================================================

BAD_WORDS = [
    "চুদ",
    "চুদা",
    "চুদাচুদি",
    "চুদানি",
    "চোদা",
    "চোদাচুদি",
    "মাদারচোদ",
    "মাদারফাকার",
    "বাল",
    "বাঞ্চোদ",
    "বানচোদ",
    "হারামজাদা",
    "হারামি",
    "কুত্তারবাচ্চা",
    "কুত্তার বাচ্চা",
    "শুয়োরের বাচ্চা",
    "শুয়োরের বাচ্চা",
    "খানকির পোলা",
    "খানকিরপোলা",
    "চোদন",
    "fuck",
    "fucking",
    "motherfucker",
    "bitch",
    "bastard",
    "asshole",
]


# =========================================================
# TEXT NORMALIZE
# =========================================================

def normalize_text(text):

    return (
        text.lower()
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace("-", "")
        .replace("_", "")
    )


def contains_bad_language(text):

    normalized = normalize_text(text)

    for word in BAD_WORDS:

        if normalize_text(word) in normalized:
            return True

    return False


# =========================================================
# CHECK ADMIN
# =========================================================

async def is_admin(update, context):

    if not update.effective_chat:
        return False

    if not update.effective_user:
        return False

    try:

        member = await context.bot.get_chat_member(
            update.effective_chat.id,
            update.effective_user.id
        )

        return member.status in [
            "administrator",
            "creator"
        ]

    except Exception as e:

        print("ADMIN CHECK ERROR:", repr(e))
        return False


# =========================================================
# WELCOME NEW MEMBER
# =========================================================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.chat_member:
        return

    new_member = update.chat_member.new_chat_member
    old_member = update.chat_member.old_chat_member

    if new_member.status not in [
        "member",
        "restricted"
    ]:
        return

    if old_member.status in [
        "member",
        "administrator",
        "creator"
    ]:
        return

    user = new_member.user

    name = user.first_name or "বন্ধু"

    text = f"""
🎉 স্বাগতম {name}! ❤️

🇧🇩 {COMMUNITY_NAME}-এ আপনাকে স্বাগতম।

🤖 আমি RJ Team-এর AI Assistant।

📚 সুন্দরভাবে কথা বলুন এবং গ্রুপের নিয়ম মেনে চলুন।

{GROUP_NOTICE}
"""

    try:

        await update.effective_chat.send_message(
            text
        )

    except Exception as e:

        print("WELCOME ERROR:", repr(e))


# =========================================================
# MODERATION
# =========================================================

async def moderate_message(
    update,
    context
):

    if not update.message:
        return False

    chat = update.effective_chat
    user = update.effective_user

    if not chat or not user:
        return False

    # Private chat নয়
    if chat.type not in [
        "group",
        "supergroup"
    ]:
        return False

    # Adminদের message বাদ
    if await is_admin(update, context):
        return False

    text = update.message.text or ""

    if not text:
        return False

    # গালাগালি নেই
    if not contains_bad_language(text):
        return False

    warnings = context.application.bot_data.setdefault(
        "bad_language_warnings",
        {}
    )

    key = (
        chat.id,
        user.id
    )

    count = warnings.get(key, 0) + 1

    warnings[key] = count

    # Delete message
    try:

        await update.message.delete()

    except Exception as e:

        print("DELETE ERROR:", repr(e))

    # =====================================================
    # FIRST WARNING
    # =====================================================

    if count == 1:

        try:

            await chat.send_message(
                f"""
⚠️ সতর্কবার্তা!

👤 {user.first_name}

আপনার মেসেজে গালাগালি/অশালীন ভাষা পাওয়া গেছে।

🚫 অনুগ্রহ করে গালাগালি করবেন না।
🤝 সবাইকে সম্মান করুন।

🕌 গ্রুপের নিয়ম:
• গালাগালি নয়
• অপমান নয়
• অশালীন কথা নয়
• সবাইকে সম্মান করুন

⚠️ দ্বিতীয়বার নিয়ম ভঙ্গ করলে আপনাকে Group থেকে Kick করা হতে পারে।
"""
            )

        except Exception as e:

            print("WARNING ERROR:", repr(e))

        return True

    # =====================================================
    # SECOND WARNING → KICK
    # =====================================================

    if count >= 2:

        try:

            await context.bot.ban_chat_member(
                chat.id,
                user.id
            )

            await context.bot.unban_chat_member(
                chat.id,
                user.id,
                only_if_banned=True
            )

            await chat.send_message(
                f"""
🚨 Group থেকে Kick করা হয়েছে

👤 {user.first_name}

আপনি দ্বিতীয়বার গালাগালি/অশালীন ভাষা ব্যবহার করেছেন।

🕌 অনুগ্রহ করে সুন্দর ভাষায় কথা বলুন এবং অন্যদের সম্মান করুন।
"""
            )

        except Exception as e:

            print("KICK ERROR:", repr(e))

            try:

                await chat.send_message(
                    f"""
⚠️ {user.first_name}, দ্বিতীয়বার নিয়ম ভঙ্গ হয়েছে।

❗ Bot-এর প্রয়োজনীয় permission না থাকায় Kick করা সম্ভব হয়নি।

👮 Group Admin-এর সাহায্য নিন।
"""
                )

            except Exception:
                pass

        warnings[key] = 0

        return True

    return True


# =========================================================
# /START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = f"""
🤖 আসসালামু আলাইকুম!

🌟 স্বাগতম {COMMUNITY_NAME}-এর AI Assistant-এ।

👤 Creator: {CREATOR_NAME}
👑 Owner: {OWNER_USERNAME}

✨ আমি আপনার প্রশ্নের উত্তর দিতে পারি।

📚 Education
💻 Technology
💰 Business
❤️ Feelings
💡 Information
🌐 Translation
🎉 Entertainment

👇 যেকোনো প্রশ্ন লিখুন।
"""

    await update.message.reply_text(text)


# =========================================================
# /HELP
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = """
📚 RJ Team Bot Help

/start
➡️ Bot শুরু করুন

/help
➡️ Help menu

/about
➡️ Bot সম্পর্কে জানুন

/owners
➡️ Owner & Team information

/reset
➡️ AI conversation reset

🌐 AI উত্তর পাওয়ার পর Translate button ব্যবহার করুন।

👥 Group-এ গালাগালি করলে moderation system কাজ করবে।
"""

    await update.message.reply_text(text)


# =========================================================
# /ABOUT
# =========================================================

async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = f"""
🤖 RJ Team AI Assistant

🇧🇩 Community:
{COMMUNITY_NAME}

👤 Creator:
{CREATOR_NAME}

👑 Owner:
{OWNER_USERNAME}

🤝 Partner:
{PARTNER_USERNAME}

🛠 Assistant:
{ASSISTANT_USERNAME}

🎵 TikTok:
{TIKTOK_USERNAME}

▶️ YouTube:
@rakib22

✨ আমি RJ Team-এর AI Assistant।
"""

    await update.message.reply_text(text)


# =========================================================
# /OWNERS
# =========================================================

async def owners(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = f"""
👑 RJ Team Team

🇧🇩 {COMMUNITY_NAME}

👤 Creator
{CREATOR_NAME}

👑 Owner
{OWNER_USERNAME}

🤝 Partner
{PARTNER_USERNAME}

🛠 Assistant
{ASSISTANT_USERNAME}

🎵 TikTok
{TIKTOK_USERNAME}

▶️ YouTube
@rakib22
"""

    keyboard = [
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
                "🛠 Assistant",
                url="https://t.me/Apple20237"
            )
        ],
        [
            InlineKeyboardButton(
                "🎵 TikTok",
                url="https://www.tiktok.com/@lyrics.song333"
            )
        ],
        [
            InlineKeyboardButton(
                "▶️ YouTube",
                url=YOUTUBE_URL
            )
        ],
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# /RESET
# =========================================================

async def reset(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["history"] = []

    await update.message.reply_text(
        "♻️ আপনার AI conversation memory reset করা হয়েছে।"
    )


# =========================================================
# CREATOR QUESTION
# =========================================================

def is_creator_question(text):

    text = text.lower()

    keywords = [
        "ke baniyeche",
        "ke banayche",
        "ke toiri koreche",
        "ke toyri koreche",
        "creator ke",
        "owner ke",
        "tomake ke baniyeche",
        "tomake ke banayche",
        "আপনাকে কে বানিয়েছে",
        "তোমাকে কে বানিয়েছে",
        "কে বানিয়েছে",
        "কে তৈরি করেছে",
        "নির্মাতা কে",
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


async def creator_answer(
    update: Update
):

    text = f"""
🤖 আমাকে তৈরি করেছে

🇧🇩 **{COMMUNITY_NAME}**

👤 Creator:
**{CREATOR_NAME}**

👑 Owner:
**{OWNER_USERNAME}**

🤝 Partner:
**{PARTNER_USERNAME}**

🛠 Assistant:
**{ASSISTANT_USERNAME}**

✨ আমি RJ Team-এর AI Assistant।
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "👑 Owner",
                url="https://t.me/RJteam1"
            ),
            InlineKeyboardButton(
                "🤝 Partner",
                url="https://t.me/Apple20237"
            )
        ],
        [
            InlineKeyboardButton(
                "🎵 TikTok",
                url="https://www.tiktok.com/@lyrics.song333"
            ),
            InlineKeyboardButton(
                "▶️ YouTube",
                url=YOUTUBE_URL
            )
        ]
    ]

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# AI REPLY
# =========================================================

async def ai_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user_text = update.message.text

    if not user_text:
        return

    # Creator information
    if is_creator_question(user_text):

        await creator_answer(update)

        return

    # Typing দেখাবে
    try:

        await update.effective_chat.send_action(
            ChatAction.TYPING
        )

    except Exception:
        pass

    history = context.user_data.setdefault(
        "history",
        []
    )

    history.append({
        "role": "user",
        "content": user_text
    })

    # শুধু শেষ 12 messages রাখি
    history = history[-12:]

    context.user_data["history"] = history

    instructions = f"""
You are RJ Team AI Assistant.

Community:
{COMMUNITY_NAME}

Creator:
{CREATOR_NAME}

Owner:
{OWNER_USERNAME}

Partner:
{PARTNER_USERNAME}

Assistant:
{ASSISTANT_USERNAME}

TikTok:
{TIKTOK_USERNAME}

YouTube:
{YOUTUBE_URL}

RULES:

- Understand Bangla and Banglish.
- Default reply language is natural Bangla.
- If user writes English/Banglish, normally reply in Bangla.
- If user explicitly requests another language, use that language.
- Give accurate and helpful answers.
- Keep answers reasonably concise and fast.
- Do not invent team information.
- If asked who created you, Creator is {CREATOR_NAME} and community is {COMMUNITY_NAME}.
- Use topic-appropriate emojis, not excessive emojis.

Love:
❤️ 🥰 🌹

Education:
📚 ✍️ 🎓

Technology:
💻 🤖 ⚙️

Business:
💰 📈 💼

Success:
🎉 🥳 ✨

Warning:
⚠️ 🚨

Useful:
💡 ✅

Never encourage abusive language.
"""

    try:

        # Fast API request
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=instructions,
            input=history
        )

        answer = response.output_text.strip()

        if not answer:

            answer = (
                "দুঃখিত 😊 এখন উত্তর তৈরি করতে পারছি না।"
            )

        # Save answer
        history.append({
            "role": "assistant",
            "content": answer
        })

        context.user_data["history"] = history[-12:]

        # Translation-এর জন্য save
        context.user_data["last_answer"] = answer

        # Telegram limit
        chunks = [
            answer[i:i + 4000]
            for i in range(
                0,
                len(answer),
                4000
            )
        ]

        for index, chunk in enumerate(chunks):

            await update.message.reply_text(
                chunk,
                reply_markup=(
                    translate_keyboard()
                    if index == len(chunks) - 1
                    else None
                )
            )

    except Exception as e:

        print("AI ERROR:", repr(e))

        await update.message.reply_text(
            "⚠️ AI উত্তর দিতে সমস্যা হয়েছে। একটু পরে আবার চেষ্টা করুন।"
        )


# =========================================================
# ONE TEXT HANDLER
# =========================================================

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not update.message.text:
        return

    # আগে moderation
    moderated = await moderate_message(
        update,
        context
    )

    if moderated:
        return

    # তারপর AI
    await ai_reply(
        update,
        context
    )


# =========================================================
# TRANSLATE MENU
# =========================================================

async def translate_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data != "translate":
        return

    await query.message.reply_text(
        "🌐 কোন ভাষায় Translate করতে চান?",
        reply_markup=language_keyboard()
    )


# =========================================================
# TRANSLATE
# =========================================================

async def language_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    language = LANGUAGES.get(
        query.data
    )

    if not language:
        return

    original = context.user_data.get(
        "last_answer"
    )

    if not original:

        await query.message.reply_text(
            "⚠️ Translate করার মতো কোনো AI উত্তর পাওয়া যায়নি।"
        )

        return

    try:

        # Translation request
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=(
                f"Translate the user's text into {language}. "
                "Preserve the meaning. "
                "Return ONLY the translation."
            ),
            input=original
        )

        translated = response.output_text.strip()

        if not translated:
            raise RuntimeError(
                "Empty translation response"
            )

        await query.message.reply_text(
            f"🌐 {language}\n\n{translated}"
        )

    except Exception as e:

        print(
            "TRANSLATE ERROR:",
            repr(e)
        )

        await query.message.reply_text(
            "⚠️ Translation করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।"
        )


# =========================================================
# MAIN
# =========================================================

async def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    if not OPENAI_API_KEY:

        raise RuntimeError(
            "OPENAI_API_KEY environment variable is missing."
        )

    # Render health server
    Thread(
        target=start_health_server,
        daemon=True
    ).start()

    # Telegram Application
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    app.add_handler(
        CommandHandler(
            "about",
            about
        )
    )

    app.add_handler(
        CommandHandler(
            "owners",
            owners
        )
    )

    app.add_handler(
        CommandHandler(
            "reset",
            reset
        )
    )

    # New member welcome
    app.add_handler(
        ChatMemberHandler(
            welcome_new_member,
            ChatMemberHandler.CHAT_MEMBER
        )
    )

    # IMPORTANT:
    # শুধু একটি normal text handler
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text,
            block=False
        )
    )

    # Translate menu
    app.add_handler(
        CallbackQueryHandler(
            translate_callback,
            pattern="^translate$"
        )
    )

    # Translation languages
    app.add_handler(
        CallbackQueryHandler(
            language_callback,
            pattern="^lang_"
        )
    )

    print("🤖 RJ Team Bot is starting...")

    await app.initialize()

    await app.start()

    await app.updater.start_polling(
        allowed_updates=Update.ALL_TYPES
    )

    print("✅ RJ Team Bot is LIVE!")

    try:

        await asyncio.Event().wait()

    finally:

        await app.updater.stop()
        await app.stop()
        await app.shutdown()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())