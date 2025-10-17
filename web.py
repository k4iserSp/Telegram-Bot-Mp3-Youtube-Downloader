from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo ✅"

def run_flask():
    app.run(host="0.0.0.0", port=10000)  # Puerto que Render detecta

# Correr Flask en un hilo separado para que no bloquee el bot
threading.Thread(target=run_flask).start()
