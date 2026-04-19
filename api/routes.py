from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
import traceback
from services.llm_client import LLMError
from services.travel_planner import plan_trip

router = APIRouter()

class TripRequest(BaseModel):
    destination: str
    num_days: int = 7
    preferences: Optional[str] = None
    reference_urls: Optional[List[str]] = []

@router.post("/plan-trip")
def create_trip_plan(request: TripRequest):
    """
    Endpoint to receive trip requests from the frontend and generate structured itineraries.
    """
    try:
        result = plan_trip(request.model_dump())
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except LLMError as e:
        logging.error(f"LLMError: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
