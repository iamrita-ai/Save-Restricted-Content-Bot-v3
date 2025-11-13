import os
import threading
from flask import Flask
from shared_client import start_client

# Flask app (keeps Render port open)
app = Flask(__name__)

@app.route('/')
def home():
    return "💞 Serena Save Bot is alive and running successfully on Render!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Run Flask in background thread
    threading.Thread(target=run_flask).start()
    # Start Telegram bot
    start_client()
