# app.py - optional; a minimal Flask wrapper if something references app.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h3>Serena Save Bot — Web endpoint</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 8080)))
