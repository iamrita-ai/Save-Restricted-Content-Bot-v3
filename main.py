# main.py
# Render-friendly entrypoint: runs Flask (for port) and starts Pyrogram bot + plugins
import os
import asyncio
import threading
import importlib
from flask import Flask
from shared_client import start_client  # async function that returns started Client
import traceback

# Flask app to keep Render port open and for health checks
app = Flask(__name__)

@app.route("/")
def home():
    return "<h3>✅ Bot service is live. Serena Save Bot running.</h3>"

# ---------------- Plugin loader and bot runner ----------------
async def load_and_run_plugins():
    """
    Start client (from shared_client.start_client) then dynamically load plugins
    and call their run_{plugin}_plugin coroutine if present.
    This preserves original repo plugin behavior.
    """
    # start_client() should be an awaitable that starts and returns a running client
    client = await start_client()

    plugin_dir = "plugins"
    if not os.path.isdir(plugin_dir):
        print(f"[INFO] No plugins folder found at '{plugin_dir}'. Continuing with core bot only.")
        # keep the client alive
        return client

    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            func_name = f"run_{plugin}_plugin"
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                if asyncio.iscoroutinefunction(func):
                    print(f"[PLUGIN] Running coroutine plugin: {plugin}")
                    # run plugin coroutine and wait for it to complete (original behavior)
                    await func()
                else:
                    # if plugin exposes a normal function, run it in executor to avoid blocking
                    print(f"[PLUGIN] Running sync plugin in executor: {plugin}")
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, func)
            else:
                print(f"[PLUGIN] No entry function '{func_name}' in plugins.{plugin}")
        except Exception as e:
            print(f"[ERROR] Failed to load/run plugin '{plugin}': {e}")
            traceback.print_exc()

    return client

# ---------------- Run both Flask and bot ----------------
async def run_all():
    # Start Flask server in a dedicated daemon thread (non-blocking)
    def _run_flask():
        port = int(os.getenv("PORT", 8080))
        # disable reloader and debug - ensures single server thread
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

    threading.Thread(target=_run_flask, daemon=True).start()
    print("[WEB] Flask web server started in background thread (port {})".format(os.getenv("PORT", 8080)))

    # Start bot + plugins
    try:
        client = await load_and_run_plugins()
        print("🚀 Bot and plugins started successfully.")
    except Exception as e:
        print(f"[FATAL] Exception while starting bot/plugins: {e}")
        traceback.print_exc()
        # to surface error in logs and stop if desired, re-raise or just keep alive:
        # raise

    # keep main event loop alive forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except (KeyboardInterrupt, SystemExit):
        print("Stopping service (keyboard/system exit).")
    except Exception as e:
        print(f"[FATAL] Unhandled exception in main: {e}")
        traceback.print_exc()
