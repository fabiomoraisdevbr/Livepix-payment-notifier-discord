from flask import Flask, request, jsonify
from threading import Thread
from cache import set_cache, get_cache
import time

app = Flask('')

trigger_function = None  

@app.route('/')
def home():
    return "bot ok"

@app.route('/message/test')
def message():
    if trigger_function:
        trigger_function()
        return "mensagem enviada"
    return "erro: trigger não definido"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "invalid payload"}), 400

    resource = data.get("resource", {})
    payment_id = resource.get("id")
    payment_type = resource.get("type")

    if payment_type != "message":
         return jsonify({"status": "ok"}), 200

    set_cache(
        "payment_" + payment_id,
        {
            "type": payment_type,
            "created_at": time.time()
        },
        ttl=300
    )

    print("WEBHOOK OK")

    return jsonify({"status": "ok"}), 200


def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive(trigger):
    global trigger_function
    trigger_function = trigger

    t = Thread(target=run)
    t.start()