"""
Achievement routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth
from app.services.achievement_service import AchievementService
from typing import List, Dict

router = APIRouter()
achievement_service = AchievementService()


@router.get("/", response_model=List[Dict])
async def get_my_achievements(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get all achievements for current user"""
    return achievement_service.get_user_achievements(current_user.id, db)


@router.get("/stats")
async def get_achievement_stats(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get achievement statistics for current user"""
    return achievement_service.get_achievement_stats(current_user.id, db)


@router.post("/check")
async def check_achievements(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Manually check and unlock new achievements"""
    newly_unlocked = achievement_service.check_and_unlock_achievements(
        current_user.id, db
    )
    
    # Send notifications for new achievements
    if newly_unlocked:
        from app.routers.websocket import broadcast_achievement
        from app.services.email_service import EmailService
        
        email_service = EmailService()
        for achievement in newly_unlocked:
            # Broadcast via WebSocket
            await broadcast_achievement(current_user.id, achievement)
            
            # Send email
            if current_user.email:
                email_service.send_achievement_email(
                    current_user.email,
                    current_user.full_name or current_user.username,
                    achievement
                )
    
    return {
        "newly_unlocked": newly_unlocked,
        "count": len(newly_unlocked)
    }


