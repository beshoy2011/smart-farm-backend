"""
Notification routes for push notifications and alerts
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth
from typing import Optional

router = APIRouter()


class FCMTokenRequest(BaseModel):
    token: str


@router.post("/register-token")
async def register_fcm_token(
    request: FCMTokenRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Register FCM token for push notifications"""
    current_user.fcm_token = request.token
    db.commit()
    return {"message": "Token registered successfully", "status": "success"}


@router.get("/token")
async def get_fcm_token(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get current FCM token"""
    return {
        "has_token": bool(current_user.fcm_token),
        "token": current_user.fcm_token if current_user.fcm_token else None
    }


@router.delete("/token")
async def delete_fcm_token(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete FCM token"""
    current_user.fcm_token = None
    db.commit()
    return {"message": "Token deleted successfully", "status": "success"}


