# File: app/models/string_theory.py
from dataclasses import dataclass, asdict
import numpy as np
from typing import List, Dict, Literal
import logging

logger = logging.getLogger(__name__)

TopologyType = Literal["Calabi-Yau", "Torus", "Orbifold", "K3"]

@dataclass
class StringTheorySystem:
    dimensions: int = 10
    tension: float = 1.0
    coupling: float = 0.1
    alpha_prime: float = 1.0
    compactification: Dict = None
    
    # Topology effects on mass spectrum
    TOPOLOGY_FACTORS = {
        "Calabi-Yau": 1.0,  # Standard case
        "Torus": 0.8,       # Simpler topology
        "Orbifold": 1.2,    # More complex spectrum
        "K3": 1.5           # Rich structure with supersymmetry
    }

    def __post_init__(self):
        if self.compactification is None:
            self._reset_compactification()
        self._validate()

    def _validate(self) -> None:
        """Validate all parameters"""
        self._validate_dimensions()
        self._validate_physics_params()

    def _validate_dimensions(self) -> None:
        """Validate dimension constraints"""
        if not 4 <= self.dimensions <= 26:
            raise ValueError("Dimensions must be between 4 and 26")
        self._reset_compactification()

    def _validate_physics_params(self) -> None:
        """Validate physical parameters"""
        if self.tension <= 0:
            raise ValueError("Tension must be positive")
        if self.coupling <= 0:
            raise ValueError("Coupling must be positive")
        if self.alpha_prime <= 0:
            raise ValueError("Alpha prime must be positive")

    def _reset_compactification(self) -> None:
        """Initialize compactification with proper number of dimensions"""
        extra_dims = self.dimensions - 4  # Spacetime has 4 large dimensions
        self.compactification = {
            'radius': [1.0] * extra_dims,  # One radius per extra dimension
            'topology': "Calabi-Yau",      # Default topology
            'metric': self._generate_metric(extra_dims)
        }

    def _generate_metric(self, dims: int) -> List[List[float]]:
        """Generate a simplified metric for the compact dimensions"""
        # Start with diagonal metric (simple case)
        return [[1.0 if i == j else 0.0 for j in range(dims)] for i in range(dims)]

    def update_topology(self, topology: TopologyType) -> None:
        """Update the compactification topology"""
        if topology not in self.TOPOLOGY_FACTORS:
            raise ValueError(f"Unsupported topology: {topology}")
        self.compactification['topology'] = topology
        # Regenerate metric based on new topology
        dims = len(self.compactification['radius'])
        self.compactification['metric'] = self._generate_metric(dims)

    def calculate_mass_spectrum(self) -> List[float]:
        """Calculate mass spectrum with topology effects"""
        try:
            n_states = 10
            n = np.arange(n_states)
            
            # Initialize masses array
            masses = np.zeros_like(n, dtype=float)
            
            # Calculate for excited states (n > 0)
            excited_states = n[1:]
            dimensional_factor = np.sqrt(self.dimensions / 10)
            topology_factor = self.TOPOLOGY_FACTORS[self.compactification['topology']]
            
            # Level factor with topology effects
            level_factor = np.sqrt(excited_states / self.alpha_prime)
            tension_factor = np.sqrt(self.tension)
            
            # Combine all factors for excited states
            masses[1:] = (level_factor * tension_factor * 
                         dimensional_factor * topology_factor)
            
            # Ground state remains at zero
            masses[0] = 0.0
            
            return masses.tolist()
        except Exception as e:
            logger.error(f"Error calculating mass spectrum: {str(e)}")
            return []

    def update_parameters(self, params: Dict) -> None:
        """Update system parameters while maintaining consistency"""
        try:
            if "topology" in params:
                self.update_topology(params["topology"])
            
            if "dimensions" in params:
                self.dimensions = int(params["dimensions"])
                self._validate()

            for key, value in params.items():
                if hasattr(self, key) and key not in ["compactification", "topology"]:
                    if key == "dimensions":
                        continue  # Already handled
                    setattr(self, key, float(value))
                elif key == "compactification_radius":
                    radius = float(value)
                    self.compactification["radius"] = [radius] * (self.dimensions - 4)
            
            logger.info(f"Parameters updated: {params}")
        except Exception as e:
            logger.error(f"Error updating parameters: {str(e)}")
            raise ValueError(f"Invalid parameters: {str(e)}")

    def to_dict(self) -> Dict:
        return asdict(self)