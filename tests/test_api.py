import pytest
from httpx import AsyncClient
from app.main import app
import asyncio

pytestmark = pytest.mark.asyncio

# Base tests
async def test_get_system_state():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/string-theory/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "success"
        assert "data" in data
        # Verify required fields in the response
        assert all(key in data["data"] for key in [
            "dimensions",
            "tension",
            "coupling",
            "alpha_prime",
            "compactification",
            "mass_spectrum",
            "timestamp"
        ])

# Parameter update tests
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
        assert data["data"]["tension"] == 1.5
        assert data["data"]["coupling"] == 0.2
        assert data["data"]["alpha_prime"] == 1.2

async def test_invalid_parameters():
    async with AsyncClient(app=app, base_url="http://test") as client:
        params = {
            "dimensions": 3,  # Invalid: must be >= 4
            "tension": -1.0,  # Invalid: must be > 0
        }
        response = await client.post("/api/v1/string-theory/update", json=params)
        assert response.status_code == 422  # Unprocessable Entity
        error_data = response.json()
        assert "detail" in error_data

# Stability tests
async def test_partial_updates():
    """Test that partial updates only modify specified parameters."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, get initial state
        initial_response = await client.get("/api/v1/string-theory/")
        initial_state = initial_response.json()["data"]
        
        # Update only one parameter
        update_params = {"tension": 2.0}
        response = await client.post("/api/v1/string-theory/update", json=update_params)
        updated_state = response.json()["data"]
        
        # Check that only tension changed
        assert updated_state["tension"] == 2.0
        assert updated_state["dimensions"] == initial_state["dimensions"]
        assert updated_state["coupling"] == initial_state["coupling"]
        assert updated_state["alpha_prime"] == initial_state["alpha_prime"]

async def test_boundary_values():
    """Test system stability with boundary values."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        test_cases = [
            {"dimensions": 4},  # Minimum valid dimensions
            {"dimensions": 26},  # Maximum valid dimensions
            {"tension": 0.000001},  # Very small tension
            {"tension": 1000000},  # Very large tension
            {"coupling": 0.000001},  # Very small coupling
            {"alpha_prime": 0.000001}  # Very small alpha prime
        ]
        
        for params in test_cases:
            response = await client.post("/api/v1/string-theory/update", json=params)
            assert response.status_code == 200, f"Failed for params: {params}"
            assert response.json()["status"] == "success"

async def test_rapid_updates():
    """Test system stability under rapid consecutive updates."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        params_list = [
            {"tension": 1.0},
            {"tension": 1.5},
            {"tension": 2.0},
            {"tension": 2.5},
            {"tension": 3.0}
        ]
        
        # Send updates in rapid succession
        tasks = [
            client.post("/api/v1/string-theory/update", json=params)
            for params in params_list
        ]
        responses = await asyncio.gather(*tasks)
        
        # Verify all updates succeeded
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "success"

async def test_mass_spectrum_consistency():
    """Test that mass spectrum calculations remain consistent."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Get initial state
        response1 = await client.get("/api/v1/string-theory/")
        spectrum1 = response1.json()["data"]["mass_spectrum"]
        
        # Get state again immediately
        response2 = await client.get("/api/v1/string-theory/")
        spectrum2 = response2.json()["data"]["mass_spectrum"]
        
        # Spectrums should be identical for same parameters
        assert spectrum1 == spectrum2
        
        # Verify spectrum is non-empty and contains valid numbers
        assert len(spectrum1) > 0
        assert all(isinstance(x, (int, float)) for x in spectrum1)
        assert all(x >= 0 for x in spectrum1)  # Physics constraint: masses should be non-negative

async def test_system_resilience():
    """Test system resilience with various edge cases."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        edge_cases = [
            {},  # Empty update
            {"unknown_param": 42},  # Unknown parameter
            {"dimensions": 11, "unknown_param": 42},  # Mix of valid and invalid
            {"dimensions": "11"},  # String instead of int
            {"tension": "1.5"},  # String instead of float
        ]
        
        for params in edge_cases:
            response = await client.post("/api/v1/string-theory/update", json=params)
            # Should either succeed or fail gracefully with 422
            assert response.status_code in [200, 422]
            
            # System should still be responsive after each edge case
            health_check = await client.get("/api/v1/string-theory/")
            assert health_check.status_code == 200