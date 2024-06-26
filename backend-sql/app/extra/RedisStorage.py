import redis
from typing import Optional
from . import config

config = config.get_config()

class RedisStorage:
    def __init__(self, host: str = config.REDIS_HOST, port: int = config.REDIS_PORT, db: int = 0):
        self._store = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str) -> Optional[str]:
        value = self._store.get(key)
        return value.decode() if value else None

    def set(self, key: str, value: str, ex: int = None) -> None:
        self._store.set(key, value, ex=ex)

    def delete(self, key: str) -> None:
        self._store.delete(key)

    def get_instance(self):
        return self._store