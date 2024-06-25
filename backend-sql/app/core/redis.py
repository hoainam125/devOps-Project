import redis
from app.core.config import settings

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def set_redis_data(key, value):
    redis_client.set(key, value)

def get_redis_data(key):
    return redis_client.get(key)
