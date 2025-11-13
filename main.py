import os
import asyncio
from flask import Flask
from pyrogram import Client, filters

# ╔══════════════════════════════════════════════════╗
#  FLASK APP — Keeps Render Port Alive (Web Service)
# ╚══════════════════════════════════════════════════╝
app = Flask(__name__)

@app.route('/')
def home():
    return "💫 Serena Save Bot is alive and running perfectly on Render 💫"


# ╔══════════════════════════════════════════════════╗
#  TELEGRAM BOT SETUP
# ╚══════════════════════════════════════════════════╝
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# Support both STRING or STRING_SESSION
SESSION = os.getenv("STRING") or os.getenv("STRING_SESSION")

if SESSION:
    bot = Client(
        "serena_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION
    )
else:
    bot = Client(
        "serena_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )


# ╔══════════════════════════════════════════════════╗
#  COMMANDS
# ╚══════════════════════════════════════════════════╝
@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "🌸 **Hello Sweetheart!**\n"
        "Your Serena Save Bot is alive & ready to work 💞\n\n"
        "— Powered by *Serena Technologies* ✨"
    )


@bot.on_message(filters.text & ~filters.command(["start"]))
async def echo(client, message):
    await message.reply_text(f"💌 You said: {message.text}")


# ╔══════════════════════════════════════════════════╗
#  COMBINE FLASK + TELEGRAM BOT
# ╚══════════════════════════════════════════════════╝
async def run_all():
    # Run Flask (web) in background
    loop = asyncio.get_event_loop()
    loop.create_task(
        loop.run_in_executor(
            None,
            lambda: app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
        )
    )

    # Start Telegram bot
    await bot.start()
    print("🚀 Serena Bot started successfully on Render!")

    # Keep running
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except Exception as e:
        print(f"❌ Error while running bot: {e}")
