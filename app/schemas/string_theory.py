# File: app/schemas/string_theory.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal

TopologyType = Literal["Calabi-Yau", "Torus", "Orbifold", "K3"]

class StringParameters(BaseModel):
    dimensions: Optional[int] = Field(None, ge=4, le=26)
    tension: Optional[float] = Field(None, gt=0)
    coupling: Optional[float] = Field(None, gt=0)
    alpha_prime: Optional[float] = Field(None, gt=0)
    compactification_radius: Optional[float] = Field(None, gt=0)
    topology: Optional[TopologyType] = None

class SystemState(BaseModel):
    dimensions: int
    tension: float
    coupling: float
    alpha_prime: float
    compactification: Dict
    mass_spectrum: List[float]
    timestamp: str

class SystemResponse(BaseModel):
    status: str
    data: SystemState