import asyncio
import importlib
import os
import sys
import threading
from flask import Flask
from shared_client import start_client

# ---------------- FLASK WEB SERVER (to keep Render port open) ---------------- #

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>✅ Team SPY Bot is Running Successfully on Render!</h2>"

def run_flask():
    """Start Flask server on Render-assigned port."""
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ---------------- TELEGRAM BOT LOGIC ---------------- #

async def load_and_run_plugins():
    """Dynamically import and run all plugins."""
    await start_client()
    plugin_dir = "plugins"
    if not os.path.isdir(plugin_dir):
        print(f"[WARNING] Plugins folder not found: {plugin_dir}")
        return

    plugins = [f[:-3] for f in os.listdir(plugin_dir)
               if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"▶ Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()
        except Exception as e:
            print(f"[ERROR] Failed to load plugin {plugin}: {e}")

async def start_bot():
    """Main async bot loop."""
    print("🚀 Starting Telegram clients and plugins...")
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)

def run_bot():
    """Run the bot event loop (thread target)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)
    finally:
        loop.close()

# ---------------- MAIN ENTRY POINT ---------------- #

if __name__ == "__main__":
    # Run bot and Flask simultaneously
    threading.Thread(target=run_bot, daemon=True).start()
    run_flask()
