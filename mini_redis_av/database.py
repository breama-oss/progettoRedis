import redis
import json
import os
from threading import Lock

class Database:
    def __init__(self):
        self.r = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True
        )
        self.lock = Lock()

    def set(self, key, value):
        with self.lock:
            self.r.set(key, value)

    def get(self, key):
        return self.r.get(key)

    def delete(self, key):
        with self.lock:
            return self.r.delete(key)

    def set_json(self, key, obj):
        self.set(key, json.dumps(obj))

    def get_json(self, key):
        val = self.get(key)
        if not val:
            return None
        try:
            return json.loads(val)
        except:
            return None

    def keys(self, prefix):
        return self.r.keys(f"{prefix}*")


db = Database()
