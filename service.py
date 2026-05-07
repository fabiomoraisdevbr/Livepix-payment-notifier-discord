
import time
import requests
import cache
import os
from dotenv import load_dotenv
import threading
import webserver
from threading import Lock
from cache import get_all_keys, set_cache, get_cache, delete_cache

cache_lock = Lock()


load_dotenv()
client_id = os.getenv("LIVE_PIX_CLIENT_ID")
client_secret = os.getenv("LIVE_PIX_CLIENT_SECRET")
trigger_function = None


def get_access_token():
    now = time.time()

    cached = get_cache("access_token")
    if cached:
        return cached["access_token"]

    url = "https://oauth.livepix.gg/oauth2/token"
    #url = "http://localhost:8081/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "payments:read messages:read webhooks"
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    res = requests.post(url, data=data, headers=headers)
    json_data = res.json()

    set_cache(
        "access_token",
        {
            "access_token": json_data["access_token"]
        },
        ttl=json_data["expires_in"]
    )

    return json_data["access_token"]


def get_payment_details(payment_id):
    token = get_access_token()

    payment = payment_id.replace("payment_", "")


    url = f"https://api.livepix.gg/v2/messages/{payment}"
    #url = f"http://localhost:8081/v2/payments/{payment}"

    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json"
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    data = res.json().get("data")
    if not data:
        raise ValueError("Resposta sem campo data")

    amount = data.get("amount")
    currency = data.get("currency")
    user_name = data.get("username")
    message = data.get("message")

    if amount is None or currency is None:
        raise ValueError("Resposta sem amount ou currency")

    set_cache(
        f"payment_details_{payment_id}",
        {
            "amount": amount,
            "currency": currency,
            "user_name": user_name,
            "message": message
        },
        ttl=300
    )

    delete_cache(payment_id)

    if webserver.trigger_function:
        webserver.trigger_function()



def is_a_payment_in_cache():
    while True:
        time.sleep(5)
        print("chegando pagamentos no cache...")

        keys = get_all_keys()

        for key in keys:
            if key.startswith("payment_"):
                get_payment_details(key)


                

threading.Thread(target=is_a_payment_in_cache, daemon=True).start()
