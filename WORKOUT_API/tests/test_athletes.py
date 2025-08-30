import pytest

@pytest.mark.asyncio
async def test_list_athletes_empty(client):
    r = await client.get("/athletes")
    assert r.status_code == 200
    assert r.json() == []