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
            self.compactification = {
                'radius': [1.0] * 6,  # Compactification radii for 6 extra dimensions
                'topology': 'Calabi-Yau'
            }
    
    def calculate_mass_spectrum(self) -> List[float]:
        try:
            n = np.arange(10)
            return np.sqrt(n / self.alpha_prime).tolist()
        except Exception as e:
            logger.error(f"Error calculating mass spectrum: {str(e)}")
            return []
    
    def update_parameters(self, params: Dict) -> None:
        try:
            for key, value in params.items():
                if hasattr(self, key) and key != 'compactification':
                    setattr(self, key, float(value))
                elif key == 'compactification_radius':
                    self.compactification['radius'] = [float(value)] * 6
            logger.info(f"Parameters updated: {params}")
        except Exception as e:
            logger.error(f"Error updating parameters: {str(e)}")
            raise ValueError(f"Invalid parameters: {str(e)}")

    def to_dict(self) -> Dict:
        return asdict(self)