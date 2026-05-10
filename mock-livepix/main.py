from flask import Flask, request, jsonify
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "bot ok"

@app.route('/v2/messages/<message>', methods=['GET'])
def get_payment(message):
  return jsonify({
    "data": {
        "id": message,
        "proof": "E0000000020210727170449258921630",
        "reference": "foo",
        "amount": 1000,
        "currency": "BRL",
        "createdAt": "2021-01-01T00:00:00-03:00"
    }
})

@app.route('/oauth2/token', methods=['POST'])
def oauth_token():
    return jsonify({
        "access_token": "ory_at_rYoC8xJ3y4Kr_TwH7073CogddYI5PE_A3uTRZpfuQ_0.emePDgEQRCqigPRHdi2u1g5tAxdbjw_gbP1A6g94ByM",
        "expires_in": 3599,
        "scope": "payments:read messages:read webhooks",
        "token_type": "bearer"
    })

def run():
    app.run(host="0.0.0.0", port=8081)

def keep_alive():

    t = Thread(target=run)
    t.start()

keep_alive()