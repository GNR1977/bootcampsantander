import asyncio
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app as fastapi_app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture
async def client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac