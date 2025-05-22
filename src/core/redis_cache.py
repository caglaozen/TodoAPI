import json
import os

import redis


class RedisCache:
    def __init__(self):
        host = os.environ.get("REDIS_HOST", "redis")
        port = int(os.environ.get("REDIS_PORT", 6379))

        try:
            self.redis_client = redis.Redis(host=host, port=port)
            self.redis_client.ping()
        except redis.ConnectionError as e:
            print(f"Warning: Could not connect to Redis: {e}")
            print("Application will continue, but caching will not work")
            self.redis_client = None

    def get(self, key):
        if not self.redis_client:
            return None

        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def set(self, key, value):
        if not self.redis_client:
            return

        try:
            self.redis_client.set(key, json.dumps(value, default=lambda obj: obj.__dict__))
        except Exception as e:
            print(f"Redis set error: {e}")

    def delete(self, key):
        if not self.redis_client:
            return False

        try:
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
