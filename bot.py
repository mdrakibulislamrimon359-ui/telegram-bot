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

from telegram.constants import ChatMemberStatus

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
    filters,
)


# ============================================================
# RJ TEAM BOT SETTINGS
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)

PORT = int(
    os.getenv("PORT", "10000")
)


# ============================================================
# RJ TEAM INFORMATION
# ============================================================

COMMUNITY_NAME = "RJ Team Bangladesh Community"

CREATOR_NAME = "Rakib Sar"

OWNER_USERNAME = "@RJteam1"

PARTNER_USERNAME = "@Apple20237"

ASSISTANT_USERNAME = "@Apple20237"

TIKTOK_USERNAME = "lyrics.song333"

YOUTUBE_LINK = "https://youtube.com/@rakib22"


# ============================================================
# CHECK ENVIRONMENT VARIABLES
# ============================================================

if not BOT_TOKEN:

    raise RuntimeError(
        "BOT_TOKEN is missing"
    )


if not OPENAI_API_KEY:

    raise RuntimeError(
        "OPENAI_API_KEY is missing"
    )


client = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)


# ============================================================
# RENDER HEALTH SERVER
# ============================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            b"RJ Team Bot is running!"
        )

    def log_message(
        self,
        format,
        *args
    ):

        pass


def start_health_server():

    server = HTTPServer(
        ("0.0.0.0", PORT),
        HealthHandler
    )

    server.serve_forever()


# ============================================================
# TRANSLATE BUTTON
# ============================================================

def translate_keyboard():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🌐 Translate",
                callback_data="translate"
            )
        ]

    ])


# ============================================================
# LANGUAGE KEYBOARD
# ============================================================

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


# ============================================================
# GROUP NOTICE
# ============================================================

GROUP_NOTICE = """
🌙 **RJ TEAM BANGLADESH COMMUNITY** 🇧🇩

🤝 **আসুন, সবাই সুন্দর ভাষায় কথা বলি।**

❌ গালাগালি
❌ অশ্লীল কথা
❌ কাউকে অপমান করা
❌ খারাপ নামে ডাকা
❌ হেয় করা বা বিদ্রূপ করা
❌ অসম্মানজনক আচরণ

✅ ভদ্রভাবে কথা বলুন
✅ সবাইকে সম্মান করুন
✅ মতের অমিল হলেও সুন্দরভাবে কথা বলুন
✅ ভালো কথা বলুন
✅ সুন্দর পরিবেশ তৈরি করুন 🌸

📖 **ইসলামের শিক্ষা**

আল্লাহ তাআলা বলেন:

একে অপরকে উপহাস করো না এবং একে অপরকে অপমান করো না বা মন্দ নামে ডেকো না।

— **সূরা আল-হুজুরাত ৪৯:১১**

🕌 রাসুলুল্লাহ ﷺ বলেছেন:

**“মুমিন গালিদাতা, অভিশাপদাতা, অশ্লীলভাষী বা কুরুচিপূর্ণ ভাষার মানুষ নয়।”**

— **জামে তিরমিজি ১৯৭৭**

⚠️ **RJ Team Group Rule**

🥇 ১ম বার → ⚠️ সতর্কবার্তা

🥈 ২য় বার → 🚫 Group থেকে Kick

🌸 সুন্দর কথা বলুন।
🤝 সবাইকে সম্মান করুন।

🇧🇩 **RJ Team Bangladesh Community**
"""


# ============================================================
# BAD WORD LIST
# ============================================================

BAD_WORDS = [

    # Bangla

    "চোদা",
    "চোদন",
    "চুদ",
    "চুদা",
    "চুদতে",
    "চুদবি",
    "চুদবো",
    "চুদমারানি",
    "খানকি",
    "খানকির",
    "বাঞ্চোদ",
    "বাল",
    "বালের",
    "হারামজাদা",
    "হারামি",
    "শুয়োর",
    "কুত্তা",
    "কুত্তার",
    "মাদারচোদ",
    "বেশ্যা",
    "জারজ",

    # Banglish

    "chod",
    "choda",
    "chudan",
    "chud",
    "chodbi",
    "chodbo",
    "madarchod",
    "banchod",
    "khanki",
    "haramjada",
    "harami",
    "kutta",
    "shuar",
    "beshya",
    "jaraj",

    # English

    "fuck",
    "fucking",
    "motherfucker",
    "bitch",
    "asshole",
    "bastard",
    "shit",
    "dick",
    "pussy",

]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = text.lower()

    separators = [
        " ",
        "\n",
        "\t",
        ".",
        ",",
        "!",
        "?",
        "-",
        "_",
        "*",
        "#",
        "@",
    ]

    for char in separators:

        text = text.replace(
            char,
            ""
        )

    return text


# ============================================================
# BAD LANGUAGE DETECTION
# ============================================================

def contains_bad_language(text):

    if not text:

        return False

    original = text.lower()

    normalized = normalize_text(
        text
    )

    for word in BAD_WORDS:

        if word in original:

            return True

        if word in normalized:

            return True

    return False


# ============================================================
# ADMIN CHECK
# ============================================================

async def is_admin(
    update,
    context
):

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

            ChatMemberStatus.ADMINISTRATOR,

            ChatMemberStatus.OWNER,

        ]

    except Exception as e:

        print(
            "ADMIN CHECK ERROR:",
            repr(e)
        )

        return False


# ============================================================
# WELCOME NEW MEMBER
# ============================================================

async def welcome_new_member(
    update,
    context
):

    if not update.chat_member:

        return

    chat_member = update.chat_member

    old_status = (
        chat_member.old_chat_member.status
    )

    new_status = (
        chat_member.new_chat_member.status
    )

    joined_statuses = [

        ChatMemberStatus.MEMBER,

        ChatMemberStatus.RESTRICTED,

    ]

    if new_status not in joined_statuses:

        return

    if old_status in joined_statuses:

        return

    user = (
        chat_member.new_chat_member.user
    )

    name = (
        user.first_name
        or "বন্ধু"
    )

    welcome_text = (

        f"👋 **স্বাগতম {name}!** 🌸\n\n"

        f"🇧🇩 **{COMMUNITY_NAME}**-এ আপনাকে স্বাগতম!\n\n"

        "🤝 আশা করি আপনি আমাদের সাথে সুন্দরভাবে সময় কাটাবেন।\n"

        "💬 সবাইকে সম্মান করুন এবং সুন্দর ভাষায় কথা বলুন।\n\n"

        "📜 আমাদের Group Rules ও Islamic Notice নিচে দেওয়া হলো 👇"

    )

    try:

        await context.bot.send_message(

            chat_id=update.effective_chat.id,

            text=welcome_text

        )

        await context.bot.send_message(

            chat_id=update.effective_chat.id,

            text=GROUP_NOTICE

        )

    except Exception as e:

        print(
            "WELCOME ERROR:",
            repr(e)
        )


# ============================================================
# GROUP MODERATION
# ============================================================

async def moderate_message(
    update,
    context
):

    if not update.message:

        return False

    if not update.message.text:

        return False

    chat = update.effective_chat

    if not chat:

        return False

    # IMPORTANT:
    # Private SMS is NOT moderated.

    if chat.type not in [
        "group",
        "supergroup"
    ]:

        return False

    user = update.effective_user

    if not user:

        return False

    # Admins are ignored.

    if await is_admin(
        update,
        context
    ):

        return False

    text = update.message.text

    if not contains_bad_language(
        text
    ):

        return False

    warnings = (
        context.application
        .bot_data
        .setdefault(
            "bad_language_warnings",
            {}
        )
    )

    key = (

        chat.id,

        user.id

    )

    warnings[key] = (
        warnings.get(
            key,
            0
        ) + 1
    )

    count = warnings[key]


    # --------------------------------------------------------
    # DELETE BAD MESSAGE
    # --------------------------------------------------------

    try:

        await update.message.delete()

    except Exception as e:

        print(
            "DELETE ERROR:",
            repr(e)
        )


    # --------------------------------------------------------
    # FIRST OFFENSE
    # --------------------------------------------------------

    if count == 1:

        try:

            await context.bot.send_message(

                chat_id=chat.id,

                text=(

                    "⚠️ **সতর্কবার্তা!**\n\n"

                    f"👤 {user.first_name}\n\n"

                    "❌ Group-এ গালাগালি বা অশালীন ভাষা ব্যবহার করা যাবে না।\n\n"

                    "🌸 দয়া করে ভদ্র ও সম্মানজনক ভাষায় কথা বলুন।\n\n"

                    "📌 **আর একবার এমন হলে আপনাকে Group থেকে Kick করা হবে।**"

                )

            )

        except Exception as e:

            print(
                "WARNING ERROR:",
                repr(e)
            )

        return True


    # --------------------------------------------------------
    # SECOND OFFENSE
    # --------------------------------------------------------

    if count >= 2:

        try:

            await context.bot.ban_chat_member(

                chat_id=chat.id,

                user_id=user.id

            )

            # Ban + unban = kick

            await context.bot.unban_chat_member(

                chat_id=chat.id,

                user_id=user.id,

                only_if_banned=True

            )

            await context.bot.send_message(

                chat_id=chat.id,

                text=(

                    "🚫 **Group থেকে Kick করা হয়েছে**\n\n"

                    f"👤 User: {user.first_name}\n\n"

                    "⚠️ একই ধরনের খারাপ ভাষা দ্বিতীয়বার ব্যবহার করা হয়েছে।\n\n"

                    "🌸 আমাদের Group-এ ভদ্র ও সম্মানজনক আচরণ বজায় রাখুন।\n\n"

                    "🤲 আল্লাহ আমাদের সবাইকে সুন্দর কথা বলার তাওফিক দিন।"

                )

            )

            warnings.pop(
                key,
                None
            )

        except Exception as e:

            print(
                "KICK ERROR:",
                repr(e)
            )

            try:

                await context.bot.send_message(

                    chat_id=chat.id,

                    text=(

                        "⚠️ খারাপ ভাষা শনাক্ত হয়েছে।\n\n"

                        "❌ User-কে Kick করা যায়নি।\n\n"

                        "🛡️ Bot-কে Group Admin করে "
                        "**Delete Messages** এবং "
                        "**Ban/Restrict Members** permission দিন।"

                    )

                )

            except Exception as send_error:

                print(
                    "KICK MESSAGE ERROR:",
                    repr(send_error)
                )

        return True

    return True


# ============================================================
# START
# ============================================================

async def start(
    update,
    context
):

    if not update.message:

        return

    await update.message.reply_text(

        "👋 আসসালামু আলাইকুম! 🌸\n\n"

        "🤖 আমি **RJ Team Bot**\n\n"

        "💬 আপনি আমাকে যেকোনো প্রশ্ন করতে পারেন।\n"

        "🇧🇩 আমি সাধারণভাবে বাংলায় উত্তর দেব।\n\n"

        "✨ প্রশ্নের বিষয় অনুযায়ী সুন্দর ও উপযুক্ত Emoji ব্যবহার করব।\n\n"

        "🌐 প্রতিটি AI উত্তরের নিচে Translate Button থাকবে।\n\n"

        "🚀 শুরু করতে আপনার প্রশ্ন লিখে Send করুন।"

    )


# ============================================================
# HELP
# ============================================================

async def help_command(
    update,
    context
):

    if not update.message:

        return

    await update.message.reply_text(

        "🤖 **RJ Team Bot Help**\n\n"

        "💬 যেকোনো প্রশ্ন সরাসরি লিখুন\n"

        "🇧🇩 উত্তর সাধারণভাবে বাংলায় পাবেন\n"

        "✨ প্রশ্ন অনুযায়ী সুন্দর Emoji থাকবে\n"

        "🌐 Translate দিয়ে বিভিন্ন ভাষায় অনুবাদ করতে পারবেন\n\n"

        "📌 **Commands:**\n\n"

        "▶️ /start — Bot চালু\n"

        "▶️ /help — Help\n"

        "▶️ /about — Bot সম্পর্কে\n"

        "▶️ /owners — Team Information\n"

        "▶️ /reset — Conversation memory reset"

    )


# ============================================================
# ABOUT
# ============================================================

async def about(
    update,
    context
):

    if not update.message:

        return

    await update.message.reply_text(

        "🤖 **RJ Team Bot**\n\n"

        f"🏠 Community: {COMMUNITY_NAME}\n"

        f"👤 Creator: {CREATOR_NAME}\n\n"

        f"👑 Owner: {OWNER_USERNAME}\n"

        f"🤝 Partner: {PARTNER_USERNAME}\n"

        f"🛠️ Assistant: {ASSISTANT_USERNAME}\n\n"

        f"🎵 TikTok: {TIKTOK_USERNAME}\n"

        f"▶️ YouTube: {YOUTUBE_LINK}\n\n"

        "🇧🇩 RJ Team Bangladesh Community\n"

        "✨ Smart • Friendly • Helpful"

    )


# ============================================================
# OWNERS
# ============================================================

async def owners(
    update,
    context
):

    if not update.message:

        return

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


# ============================================================
# RESET
# ============================================================

async def reset(
    update,
    context
):

    if not update.message:

        return

    context.user_data["history"] = []

    context.user_data.pop(
        "last_answer",
        None
    )

    await update.message.reply_text(

        "🧹 Conversation memory reset করা হয়েছে।\n\n"

        "✨ এখন নতুন করে কথা বলতে পারেন।"

    )


# ============================================================
# CREATOR QUESTION
# ============================================================

def is_creator_question(
    text
):

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

    return any(

        keyword in text

        for keyword in keywords

    )


# ============================================================
# CREATOR ANSWER
# ============================================================

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


# ============================================================
# AI RESPONSE
# ============================================================

async def ai_reply(
    update,
    context
):

    if not update.message:

        return

    if not update.message.text:

        return

    user_text = (
        update.message.text.strip()
    )

    if not user_text:

        return


    # --------------------------------------------------------
    # CREATOR QUESTION
    # --------------------------------------------------------

    if is_creator_question(
        user_text
    ):

        answer = creator_answer()

        sent = await update.message.reply_text(

            answer,

            reply_markup=translate_keyboard()

        )

        context.user_data[
            "last_answer"
        ] = answer

        context.user_data[
            "last_message_id"
        ] = sent.message_id

        return


    # --------------------------------------------------------
    # CONVERSATION MEMORY
    # --------------------------------------------------------

    history = (
        context.user_data
        .setdefault(
            "history",
            []
        )
    )

    history.append({

        "role": "user",

        "content": user_text

    })


    if len(history) > 20:

        history[:] = history[-20:]


    # --------------------------------------------------------
    # OPENAI
    # --------------------------------------------------------

    try:

        response = await client.responses.create(

            model=OPENAI_MODEL,

            instructions=(

                "You are RJ Team Bot, a helpful, friendly and smart "
                "Telegram AI assistant. "

                "Always answer in natural Bangla/Bengali by default, "
                "even when the user writes English or Banglish. "

                "Only use another language when the user explicitly "
                "asks for another language. "

                "Make answers useful, accurate and easy to understand. "

                "Use beautiful and relevant emojis according to the "
                "topic and mood, but do not overuse them. "

                "Education: 📚🎓✍️. "

                "Technology: 💻🤖⚙️. "

                "Business: 💰📈💼. "

                "Love and feelings: ❤️🥰🌹. "

                "Success: 🎉🏆✨. "

                "Warning: ⚠️🚨. "

                "Useful information: 💡✅. "

                "Use headings or bullets when helpful. "

                "If asked who created, made, built or owns this bot, "
                "use these facts: "

                "Created by RJ Team Bangladesh Community. "

                "Creator: Rakib Sar. "

                "Owner: @RJteam1. "

                "Partner: @Apple20237. "

                "Assistant: @Apple20237. "

                "TikTok: lyrics.song333. "

                "YouTube: https://youtube.com/@rakib22. "

                "Do not describe anyone as owner unless the user "
                "specifically asks for the owner."

            ),

            input=history

        )


        answer = (
            response.output_text
            or ""
        ).strip()


        if not answer:

            answer = (
                "😔 দুঃখিত, এখন কোনো উত্তর পাওয়া যায়নি।"
            )


        history.append({

            "role": "assistant",

            "content": answer

        })


        context.user_data[
            "last_answer"
        ] = answer


        # ----------------------------------------------------
        # TELEGRAM MESSAGE LIMIT
        # ----------------------------------------------------

        for i in range(

            0,

            len(answer),

            4000

        ):

            chunk = answer[
                i:i + 4000
            ]

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


# ============================================================
# IMPORTANT MAIN TEXT HANDLER
# ============================================================

async def handle_text(
    update,
    context
):

    if not update.message:

        return

    if not update.message.text:

        return


    # প্রথমে group moderation check হবে।
    # Private chat হলে moderate_message False করবে।

    moderated = await moderate_message(

        update,

        context

    )


    if moderated:

        return


    # Private SMS + normal group message
    # এখানে AI response যাবে।

    await ai_reply(

        update,

        context

    )


# ============================================================
# TRANSLATE MENU
# ============================================================

async def translate_button(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(

        "🌐 **কোন ভাষায় Translate করতে চান?**\n\n"

        "👇 আপনার পছন্দের ভাষায় চাপ দিন।",

        reply_markup=language_keyboard()

    )


# ============================================================
# TRANSLATE
# ============================================================

async def translate_text(
    update,
    context
):

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


        translated = (

            response.output_text
            or ""

        ).strip()


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

            "❌ Translation করতে সমস্যা হয়েছে.\n"

            "⏳ একটু পরে চেষ্টা করুন।"

        )


# ============================================================
# CLOSE TRANSLATE
# ============================================================

async def close_translate(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    try:

        await query.message.delete()

    except Exception:

        await query.message.edit_text(

            "❌ Translate menu বন্ধ করা হয়েছে।"

        )


# ============================================================
# MAIN
# ============================================================

async def main():

    # Render health server

    Thread(

        target=start_health_server,

        daemon=True

    ).start()


    # Create Telegram application

    app = (

        Application

        .builder()

        .token(BOT_TOKEN)

        .build()

    )


    # ========================================================
    # COMMANDS
    # ========================================================

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


    # ========================================================
    # NEW MEMBER WELCOME
    # ========================================================

    app.add_handler(

        ChatMemberHandler(

            welcome_new_member,

            ChatMemberHandler.CHAT_MEMBER

        )

    )


    # ========================================================
    # IMPORTANT:
    # ONLY ONE NORMAL TEXT HANDLER
    #
    # This fixes the private SMS problem.
    # ========================================================

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            handle_text,

            block=False

        )

    )


    # ========================================================
    # TRANSLATE
    # ========================================================

    app.add_handler(

        CallbackQueryHandler(

            translate_button,

            pattern=r"^translate$"

        )

    )


    app.add_handler(

        CallbackQueryHandler(

            translate_text,

            pattern=r"^lang_"

        )

    )


    app.add_handler(

        CallbackQueryHandler(

            close_translate,

            pattern=r"^close_translate$"

        )

    )


    print(
        "RJ Team Bot is running..."
    )


    # ========================================================
    # START BOT
    # ========================================================

    await app.initialize()

    await app.start()

    await app.updater.start_polling()


    try:

        await asyncio.Event().wait()

    finally:

        await app.updater.stop()

        await app.stop()

        await app.shutdown()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )