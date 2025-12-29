"""
Weekly Recommendations Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth
from app.services.weekly_recommendations_service import weekly_recommendations_service

router = APIRouter()


@router.get("/generate")
async def generate_weekly_recommendations(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Generate weekly recommendations for current user"""
    try:
        recommendations = weekly_recommendations_service.generate_recommendations(
            current_user.id, db
        )
        
        # Save to database
        weekly_recommendations_service.save_recommendations(
            current_user.id, recommendations, db
        )
        
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get("/history")
async def get_recommendations_history(
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get recommendations history"""
    try:
        recommendations = db.query(models.WeeklyRecommendation).filter(
            models.WeeklyRecommendation.user_id == current_user.id
        ).order_by(models.WeeklyRecommendation.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "week_start": r.week_start_date.isoformat(),
                "recommendations": r.recommendations,
                "created_at": r.created_at.isoformat()
            }
            for r in recommendations
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting history: {str(e)}"
        )


