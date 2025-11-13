import os
import threading
from flask import Flask
from shared_client import start_client

# Flask App for Render (keeps service alive)
app = Flask(__name__)

@app.route('/')
def home():
    return "💞 Bot is alive and running successfully on Render!"

# Flask ko alag thread me run karenge
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask server ko start karo
    threading.Thread(target=run_flask).start()
    # Telegram bot ko start karo
    start_client()
