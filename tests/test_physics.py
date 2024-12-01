import pytest
import numpy as np
from httpx import AsyncClient
from app.main import app

pytestmark = pytest.mark.asyncio

async def test_string_tension_energy_relation():
    """Test that string tension correctly affects the energy spectrum.
    E ~ T * L where T is tension and L is the string length"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with different tensions
        tensions = [1.0, 2.0, 4.0]
        spectra = []
        
        for tension in tensions:
            response = await client.post("/api/v1/string-theory/update", 
                                      json={"tension": tension})
            data = response.json()["data"]
            spectra.append(data["mass_spectrum"])
        
        # Verify energy scaling with tension
        # For doubled tension, energies should scale by √2
        for i in range(len(tensions)-1):
            # Convert to numpy arrays and exclude ground state (first element)
            spectrum1 = np.array(spectra[i])[1:]  # Excited states only
            spectrum2 = np.array(spectra[i+1])[1:]  # Excited states only
            
            # Calculate ratios for excited states only
            ratio = spectrum2 / spectrum1
            expected_ratio = np.sqrt(tensions[i+1] / tensions[i])
            
            # Test that all excited states scale properly with tension
            np.testing.assert_allclose(ratio, expected_ratio, rtol=1e-5)
            
            # Verify ground state remains at zero regardless of tension
            assert spectra[i][0] == 0.0
            assert spectra[i+1][0] == 0.0

async def test_mass_spectrum_quantization():
    """Test that the mass spectrum shows proper quantization.
    In string theory, the spectrum should be discrete and follow M² = n/α'"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/string-theory/")
        data = response.json()["data"]
        spectrum = data["mass_spectrum"]
        alpha_prime = data["alpha_prime"]

        # Convert spectrum to mass squared
        mass_squared = np.array([m**2 for m in spectrum])
        
        # Check that ratios between adjacent levels are approximately integers
        ratios = mass_squared[1:] / mass_squared[1] if len(mass_squared) > 1 else []
        np.testing.assert_allclose(ratios, np.round(ratios), rtol=1e-5)

async def test_critical_dimensions():
    """Test behavior in critical dimensions.
    Superstring theory requires 10 dimensions for consistency."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test in critical dimension (10)
        response = await client.post("/api/v1/string-theory/update", 
                                   json={"dimensions": 10})
        data = response.json()["data"]
        critical_spectrum = data["mass_spectrum"]
        
        # Test in non-critical dimension
        response = await client.post("/api/v1/string-theory/update", 
                                   json={"dimensions": 11})
        data = response.json()["data"]
        noncritical_spectrum = data["mass_spectrum"]
        
        # Verify spectra are different (tachyon-free in critical dimension)
        assert critical_spectrum != noncritical_spectrum

async def test_compactification_consistency():
    """Test that compactification parameters maintain consistency.
    Extra dimensions should be properly compactified."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/string-theory/")
        data = response.json()["data"]
        
        # Check compactification dimensions
        compactification = data["compactification"]
        assert len(compactification["radius"]) == data["dimensions"] - 4
        assert all(r > 0 for r in compactification["radius"])
        assert compactification["topology"] == "Calabi-Yau"

async def test_coupling_perturbativity():
    """Test that coupling remains in perturbative regime.
    String coupling should be small for perturbation theory validity."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with various coupling values
        couplings = [0.1, 0.5, 0.9]
        
        for g in couplings:
            response = await client.post("/api/v1/string-theory/update", 
                                      json={"coupling": g})
            data = response.json()["data"]
            spectrum = data["mass_spectrum"]
            
            # Verify spectrum remains real (no imaginary parts)
            assert all(isinstance(m, (int, float)) for m in spectrum)
            assert all(m >= 0 for m in spectrum)

async def test_energy_scale_hierarchy():
    """Test proper energy scale hierarchy.
    String scale should be well-separated from compactification scale."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/string-theory/")
        data = response.json()["data"]
        
        # String scale is ~ 1/√α'
        string_scale = 1.0 / np.sqrt(data["alpha_prime"])
        
        # Compactification scale is ~ 1/R
        comp_scale = 1.0 / data["compactification"]["radius"][0]
        
        # Verify scale separation
        assert string_scale > comp_scale

async def test_mass_gap():
    """Test for presence of mass gap in spectrum.
    String theory should exhibit a discrete mass gap."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/string-theory/")
        data = response.json()["data"]
        spectrum = data["mass_spectrum"]
        
        # Check for non-zero mass gap
        mass_differences = np.diff(spectrum)
        assert all(diff > 0 for diff in mass_differences)