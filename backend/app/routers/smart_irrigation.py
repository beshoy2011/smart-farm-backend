"""
Smart Irrigation Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.database import get_db
from app import models, auth
from app.services.smart_irrigation_service import smart_irrigation_service

router = APIRouter()


class ScheduleIrrigationRequest(BaseModel):
    analysis_id: int
    duration_minutes: int
    scheduled_time: Optional[str] = None


@router.get("/check")
async def check_irrigation_needs(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Check if irrigation is needed"""
    try:
        result = smart_irrigation_service.check_irrigation_needs(current_user.id, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/schedule")
async def schedule_irrigation(
    request: ScheduleIrrigationRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Schedule automatic irrigation"""
    try:
        scheduled_time = None
        if request.scheduled_time:
            scheduled_time = datetime.fromisoformat(request.scheduled_time)
        
        result = smart_irrigation_service.schedule_irrigation(
            current_user.id,
            request.analysis_id,
            request.duration_minutes,
            scheduled_time,
            db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/execute/{schedule_id}")
async def execute_irrigation(
    schedule_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Execute irrigation"""
    try:
        # Verify ownership
        schedule = db.query(models.IrrigationSchedule).filter(
            models.IrrigationSchedule.id == schedule_id,
            models.IrrigationSchedule.user_id == current_user.id
        ).first()
        
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        result = smart_irrigation_service.execute_irrigation(schedule_id, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/history")
async def get_irrigation_history(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get irrigation history"""
    try:
        result = smart_irrigation_service.get_irrigation_history(current_user.id, days, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/stats")
async def get_water_usage_stats(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get water usage statistics"""
    try:
        result = smart_irrigation_service.get_water_usage_stats(current_user.id, days, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

