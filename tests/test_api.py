# File: tests/test_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_system_state():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/string-theory/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "success"
        assert "data" in data

@pytest.mark.asyncio
async def test_update_parameters():
    async with AsyncClient(app=app, base_url="http://test") as client:
        params = {
            "dimensions": 11,
            "tension": 1.5,
            "coupling": 0.2,
            "alpha_prime": 1.2,
            "compactification_radius": 1.1
        }
        response = await client.post("/api/v1/string-theory/update", json=params)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["dimensions"] == 11