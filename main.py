import os
import asyncio
from flask import Flask
from pyrogram import Client, filters

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "💫 Serena Save Bot is alive on Render 💫"

# --- Telegram Client Setup ---
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# --- Client selection ---
if STRING_SESSION:
    bot = Client("serena_userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
else:
    bot = Client("serena_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Telegram Commands ---
@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "🌸 **Hello Sweetheart!**\n"
        "Your bot is alive & working perfectly 💞\n\n"
        "— Powered by Serena ✨"
    )

@bot.on_message(filters.text & ~filters.command(["start"]))
async def echo(client, message):
    await message.reply_text(f"💌 You said: {message.text}")

# --- Run both Flask & Bot together ---
async def run_all():
    # Run Flask in background
    asyncio.create_task(asyncio.to_thread(
        app.run, host="0.0.0.0", port=int(os.getenv("PORT", 8080))
    ))

    # Run Telegram bot
    await bot.start()
    print("🚀 Bot started successfully on Render!")
    await bot.idle()  # Keeps it alive

if __name__ == "__main__":
    asyncio.run(run_all())
