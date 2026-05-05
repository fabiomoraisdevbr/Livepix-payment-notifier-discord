# cache.py
import time
import threading
from threading import Lock

cache = {}
cache_lock = Lock()

def set_cache(key: str, value: dict, ttl: int):
    with cache_lock:
        cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }


def get_cache(key: str):
    with cache_lock:
        entry = cache.get(key)
        if not entry:
            return None

        if entry["expires_at"] < time.time():
            del cache[key]
            return None

        return entry["value"]


def delete_cache(key: str):
    with cache_lock:
        cache.pop(key, None)

def get_all_keys():
    with cache_lock:
        return list(cache.keys())

def cleaner():
    while True:
        time.sleep(30)
        now = time.time()

        with cache_lock:
            for key in list(cache.keys()):
                entry = cache.get(key)

                if not isinstance(entry, dict):
                    del cache[key]
                    continue

                if entry.get("expires_at", 0) < now:
                    del cache[key]

def find_first(prefix: str):
    with cache_lock:
        for key, value in cache.items():
            if key.startswith(prefix):
                return key, value
    return None, None


threading.Thread(target=cleaner, daemon=True).start()