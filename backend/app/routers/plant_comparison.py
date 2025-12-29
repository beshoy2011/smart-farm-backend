"""
Plant Comparison Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app import models, auth
from app.services.plant_comparison_service import plant_comparison_service

router = APIRouter()


class ComparisonRequest(BaseModel):
    analysis_id_1: int
    analysis_id_2: int


@router.post("/compare")
async def compare_plants(
    request: ComparisonRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two plant analyses"""
    try:
        result = plant_comparison_service.compare_plants(
            request.analysis_id_1,
            request.analysis_id_2,
            db
        )
        
        # Save comparison to database
        comparison = models.PlantComparison(
            user_id=current_user.id,
            analysis_id_1=request.analysis_id_1,
            analysis_id_2=request.analysis_id_2,
            comparison_results=result
        )
        db.add(comparison)
        db.commit()
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")


@router.get("/timeline")
async def get_timeline_comparison(
    plant_type: Optional[str] = None,
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get timeline comparison of plants"""
    try:
        result = plant_comparison_service.get_timeline_comparison(
            current_user.id,
            plant_type,
            days,
            db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Timeline error: {str(e)}")


