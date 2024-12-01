# File: app/models/string_theory.py
from dataclasses import dataclass, asdict
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

@dataclass
class StringTheorySystem:
    dimensions: int = 10
    tension: float = 1.0
    coupling: float = 0.1
    alpha_prime: float = 1.0
    compactification: Dict = None

    def __post_init__(self):
        if self.compactification is None:
            self._reset_compactification()
        self._validate_dimensions()

    def _reset_compactification(self) -> None:
        """Initialize compactification with proper number of dimensions"""
        extra_dims = self.dimensions - 4  # Spacetime has 4 large dimensions
        self.compactification = {
            'radius': [1.0] * extra_dims,  # One radius per extra dimension
            'topology': 'Calabi-Yau'
        }

    def _validate_dimensions(self) -> None:
        """Validate dimension constraints"""
        if not 4 <= self.dimensions <= 26:
            raise ValueError("Dimensions must be between 4 and 26")
        self._reset_compactification()

    def calculate_mass_spectrum(self) -> List[float]:
        """Calculate the mass spectrum according to string theory.
        
        The mass formula includes:
        - Basic string modes (n/α')
        - Tension effects (√T)
        - Dimensional corrections
        """
        try:
            # Number of oscillator states to compute
            n_states = 10
            
            # Basic oscillator spectrum (M² = n/α')
            n = np.arange(n_states)
            
            # Initialize masses array
            masses = np.zeros_like(n, dtype=float)
            
            # Calculate masses for excited states (n > 0)
            # Mass formula: M = √(n/α') * √T * dimensional_factor
            excited_states = n[1:]  # Skip n=0
            dimensional_factor = np.sqrt(self.dimensions / 10)  # Normalize to 10D
            
            # Calculate square root of (n/α') term
            level_factor = np.sqrt(excited_states / self.alpha_prime)
            
            # Include tension scaling (√T)
            tension_factor = np.sqrt(self.tension)
            
            # Combine all factors for excited states
            masses[1:] = level_factor * tension_factor * dimensional_factor
            
            # Ground state (n=0) remains at zero mass in superstring theory
            masses[0] = 0.0
            
            # Handle critical dimension effects
            if self.dimensions == 10:  # Superstring critical dimension
                masses = masses[masses >= 0]  # Remove tachyonic states
            
            return masses.tolist()
        except Exception as e:
            logger.error(f"Error calculating mass spectrum: {str(e)}")
            return []

    def update_parameters(self, params: Dict) -> None:
        """Update system parameters while maintaining consistency"""
        try:
            # Handle dimension updates first
            if "dimensions" in params:
                self.dimensions = int(params["dimensions"])
                self._validate_dimensions()

            # Update other parameters
            for key, value in params.items():
                if hasattr(self, key) and key != "compactification":
                    if key == "dimensions":
                        continue  # Already handled
                    setattr(self, key, float(value))
                elif key == "compactification_radius":
                    self.compactification["radius"] = [float(value)] * (self.dimensions - 4)
            
            logger.info(f"Parameters updated: {params}")
        except Exception as e:
            logger.error(f"Error updating parameters: {str(e)}")
            raise ValueError(f"Invalid parameters: {str(e)}")

    def to_dict(self) -> Dict:
        return asdict(self)