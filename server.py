import os
import threading
from flask import Flask
from main import start_bot  # <-- ensure your bot main function is named start_bot()

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>✅ Bot is Running Successfully on Render!</h2>"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    start_bot()

if __name__ == "__main__":
    # Run both Flask web server and Telegram bot in separate threads
    threading.Thread(target=run_bot).start()
    run_flask()
