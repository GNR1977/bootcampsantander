import json
import asyncio
import aioredis

class Cache:
    def __init__(self, url: str):
        self._url = url
        self._redis = None

    async def init(self):
        if not self._redis:
            self._redis = await aioredis.from_url(self._url, encoding="utf-8", decode_responses=True)

    async def get_json(self, key: str):
        await self.init()
        data = await self._redis.get(key)
        return json.loads(data) if data else None

    async def set_json(self, key: str, value: dict | list, ttl: int = 10):
        await self.init()
        await self._redis.set(key, json.dumps(value), ex=ttl)

cache = None

async def get_cache():
    global cache
    if cache is None:
        from pydantic_settings import BaseSettings
        class S(BaseSettings):
            REDIS_URL: str
            class Config: env_file = ".env"
        s = S()
        cache = Cache(s.REDIS_URL)
    return cache