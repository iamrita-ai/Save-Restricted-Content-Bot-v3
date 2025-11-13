import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# If STRING_SESSION exists → use userbot session, else normal bot
if STRING_SESSION:
    app = Client(
        "serena_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
    )
else:
    app = Client(
        "serena_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

# --- BOT COMMANDS ---

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "💫 **Hello Sweetheart!**\n"
        "I'm alive and working perfectly on Render ❤️\n\n"
        "✨ Powered by Serena Technologies ✨"
    )

@app.on_message(filters.text & ~filters.command(["start"]))
async def echo(client, message):
    try:
        await message.reply_text(f"💌 You said: {message.text}")
    except FloodWait as e:
        print(f"⏳ FloodWait of {e.value} seconds. Sleeping...")
        await asyncio.sleep(e.value)

# --- START CLIENT ---

def start_client():
    print("🚀 Starting Telegram bot client...")
    try:
        app.run()
    except FloodWait as e:
        print(f"⚠️ FloodWait triggered for {e.value} seconds. Retrying...")
        asyncio.sleep(e.value)
        app.run()
    except Exception as ex:
        print(f"❌ Error while running bot: {ex}")
