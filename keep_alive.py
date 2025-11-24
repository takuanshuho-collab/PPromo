from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "🤖 O Bot Espião está Online e Operante!"

def run():
    # O Render espera que a gente escute na porta 0.0.0.0
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()