"""
Advanced Analytics Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth
from app.services.advanced_analytics_service import advanced_analytics_service

router = APIRouter()


@router.get("/comprehensive")
async def get_comprehensive_stats(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive statistics"""
    try:
        result = advanced_analytics_service.get_comprehensive_stats(
            current_user.id, days, db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/comparison")
async def get_comparison_with_others(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Compare with other users (anonymized)"""
    try:
        result = advanced_analytics_service.get_comparison_with_others(
            current_user.id, db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/predictions")
async def get_predictions(
    days_ahead: int = 7,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get future predictions"""
    try:
        result = advanced_analytics_service.get_predictions(
            current_user.id, days_ahead, db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

