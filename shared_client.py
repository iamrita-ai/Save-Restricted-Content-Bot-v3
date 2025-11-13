# ===============================================
# shared_client.py — Safe Render-Ready Version
# ===============================================
import os
import asyncio
import time
from pyrogram import Client, errors as pyro_errors
from telethon import TelegramClient, errors as tele_errors

# Load environment variables
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION", None)

# Optional Mongo / Database URLs (ignore if not used)
MONGO_URL = os.getenv("MONGO_URL", None)

# ===============================================
# Function: Start both Clients (Pyrogram + Telethon)
# ===============================================

async def start_client():
    print("🚀 Starting clients...")

    # --- Pyrogram bot client ---
    bot = Client(
        "bot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        in_memory=True  # safer for Render
    )

    # --- Telethon (optional user session if provided) ---
    telethon_client = None
    if STRING_SESSION:
        try:
            telethon_client = TelegramClient(
                "telethon_session",
                API_ID,
                API_HASH
            )
            await telethon_client.start()
            print("✅ Telethon client started (owner session active)")
        except Exception as e:
            print(f"⚠️ Telethon error: {e}")

    # --- Start Pyrogram bot with safe flood handling ---
    while True:
        try:
            await bot.start()
            print("✅ Pyrogram bot started successfully!")
            break
        except pyro_errors.FloodWait as e:
            print(f"⚠️ Flood wait {e.value} seconds. Sleeping...")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"❌ Pyrogram start error: {e}")
            await asyncio.sleep(10)

    # --- Keep connection alive ---
    try:
        me = await bot.get_me()
        print(f"🤖 Logged in as: {me.first_name} (@{me.username})")
    except Exception as e:
        print(f"⚠️ Could not get bot info: {e}")

    # --- Background safety loop ---
    while True:
        try:
            await asyncio.sleep(60)
        except (pyro_errors.FloodWait, tele_errors.FloodWaitError) as e:
            print(f"⚠️ Global flood wait: {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
            await asyncio.sleep(30)

    # --- Return main clients for plugin use ---
    return bot, telethon_client
