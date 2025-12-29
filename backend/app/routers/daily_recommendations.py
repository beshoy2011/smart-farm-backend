"""
Daily Recommendations Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth
from app.services.daily_recommendations_service import daily_recommendations_service

router = APIRouter()


@router.get("/generate")
async def generate_daily_recommendations(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Generate daily recommendations"""
    try:
        result = daily_recommendations_service.generate_daily_recommendations(
            current_user.id, db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

