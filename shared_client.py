# shared_client.py
# Responsible for starting/returning a running Pyrogram Client in an async-safe way.
import asyncio
import time
import traceback
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError
import logging

# Import config variables from config.py (your repo already has this file)
try:
    from config import API_ID, API_HASH, BOT_TOKEN, STRING, OWNER_ID
except Exception:
    # fallback to env variables if config import fails
    import os
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    STRING = os.getenv("STRING", None)
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))

_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Keep a global reference so plugins can import from shared_client if needed
_client = None

async def start_client(retries: int = 5, backoff: int = 5):
    """
    Start and return a running pyrogram.Client.
    - Uses STRING (user session) if present, otherwise BOT_TOKEN.
    - Handles FloodWait and temporary errors with retry/backoff.
    - Ensures a single shared client instance.
    """
    global _client

    if _client and getattr(_client, "is_connected", False):
        _log.info("Using existing client instance.")
        return _client

    attempt = 0
    while attempt < retries:
        attempt += 1
        try:
            if STRING:
                _log.info("Starting Pyrogram user session client (STRING provided).")
                client = Client("serena_user", api_id=API_ID, api_hash=API_HASH, session_string=STRING)
            else:
                _log.info("Starting Pyrogram bot client (BOT_TOKEN).")
                client = Client("serena_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

            # start is awaitable
            await client.start()
            _log.info("Pyrogram client started and connected.")
            # sanity check: get_me
            try:
                me = await client.get_me()
                _log.info(f"Logged in as: {getattr(me, 'first_name', '')} (@{getattr(me,'username', '')})")
            except Exception:
                # not critical, continue
                _log.warning("Could not fetch 'get_me' response; continuing.")

            _client = client
            return _client

        except FloodWait as e:
            wait = getattr(e, "value", None) or getattr(e, "seconds", None) or 10
            _log.warning(f"FloodWait encountered. Sleeping for {wait} seconds (attempt {attempt}/{retries})")
            await asyncio.sleep(int(wait) + 1)
        except RPCError as e:
            _log.warning(f"Pyrogram RPCError: {e} (attempt {attempt}/{retries})")
            await asyncio.sleep(backoff * attempt)
        except Exception as e:
            _log.error(f"Unexpected error starting client: {e} (attempt {attempt}/{retries})")
            traceback.print_exc()
            await asyncio.sleep(backoff * attempt)

    raise RuntimeError("Failed to start pyrogram client after multiple attempts.")
