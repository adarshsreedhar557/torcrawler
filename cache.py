import redis
from dotenv import load_dotenv
import os

load_dotenv()

class Cache:
    def __init__(self):
        self.client = redis.StrictRedis.from_url(os.getenv("REDIS_URL"))

    def exists(self, key):
        return self.client.exists(key)

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        self.client.set(key, value)
