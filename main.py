import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters

# ---------------- Flask Server (for Render ping) ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "💫 Serena Save Bot is alive on Render 💫"

def run_flask():
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ---------------- Telegram Bot Setup ----------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# Use only bot token (no string session)
bot = Client("serena_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ---------------- Telegram Commands ----------------
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

# ---------------- Run Flask + Bot Together ----------------
async def run_all():
    # Run Flask server in a background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start Telegram bot
    await bot.start()
    print("🚀 Bot started successfully on Render!")

    # Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped manually 💔")
