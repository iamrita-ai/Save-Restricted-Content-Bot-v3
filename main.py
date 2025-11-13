import os
import threading
import asyncio
from flask import Flask
from shared_client import start_client
import importlib

app = Flask(__name__)

# --- Web server route for Render health check ---
@app.route('/')
def home():
    return "✅ Telegram Bot is Alive on Render!"

# --- Telegram bot function ---
def run_bot():
    async def load_and_run_plugins():
        await start_client()  # Start Pyrogram/Telethon client

        plugin_dir = "plugins"
        plugins = [f[:-3] for f in os.listdir(plugin_dir)
                   if f.endswith(".py") and f != "__init__.py"]

        for plugin in plugins:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"🔹 Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()

        while True:
            await asyncio.sleep(1)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(load_and_run_plugins())

# --- Start Flask and Bot Together ---
if __name__ == '__main__':
    # Start bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()

    # Start web server for Render (this keeps it alive)
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Web server running on port {port}")
    app.run(host="0.0.0.0", port=port)
