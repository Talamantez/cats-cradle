# File: app/api/v1/endpoints/string_theory.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.schemas.string_theory import StringParameters, SystemState, SystemResponse
from app.models.string_theory import StringTheorySystem
from datetime import datetime
import logging

router = APIRouter()
system = StringTheorySystem()
logger = logging.getLogger(__name__)

@router.get("/", response_model=SystemResponse)
async def get_system_state():
    """
    Get current state of the string theory system.
    """
    try:
        state = system.to_dict()
        state.update({
            'mass_spectrum': system.calculate_mass_spectrum(),
            'timestamp': datetime.utcnow().isoformat()
        })
        return {
            "status": "success",
            "data": state
        }
    except Exception as e:
        logger.error(f"Error getting system state: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.post("/update", response_model=SystemResponse)
async def update_parameters(params: StringParameters):
    """
    Update string theory system parameters.
    """
    try:
        system.update_parameters(params.dict())
        state = system.to_dict()
        state.update({
            'mass_spectrum': system.calculate_mass_spectrum(),
            'timestamp': datetime.utcnow().isoformat()
        })
        return {
            "status": "success",
            "data": state
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating parameters: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )