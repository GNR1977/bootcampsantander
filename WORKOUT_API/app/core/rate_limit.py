# app/core/rate_limit.py
from fastapi_limiter import FastAPILimiter
import aioredis
from pydantic_settings import BaseSettings

class S(BaseSettings):
    REDIS_URL: str
    class Config: env_file = ".env"

async def init_rate_limiter():
    s = S()
    redis = await aioredis.from_url(s.REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)