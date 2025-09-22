import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Bot is alive"

@app.route('/health')
def health():
    return "OK", 200

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def keep_alive():
  t = Thread(target=run)
  t.start()