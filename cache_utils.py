import os
import json
import hashlib
from datetime import datetime, timedelta

CACHE_FOLDER = ".job_cache"
CACHE_TTL_MINUTES = 15


def get_cache_key(keywords, secondary_keywords, locations, limit):
    raw = json.dumps([keywords, secondary_keywords, locations, limit], sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def load_cache(cache_key):
    path = os.path.join(CACHE_FOLDER, f"{cache_key}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
        timestamp = datetime.fromisoformat(content["timestamp"])
        if datetime.utcnow() - timestamp > timedelta(minutes=CACHE_TTL_MINUTES):
            return None
        return content["data"]
    except Exception:
        return None


def save_cache(cache_key, data):
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    path = os.path.join(CACHE_FOLDER, f"{cache_key}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"timestamp": datetime.utcnow().isoformat(), "data": data}, f)
    except Exception as e:
        print(f"❌ Failed to write cache: {e}")
