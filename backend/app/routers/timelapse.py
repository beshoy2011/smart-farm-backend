"""
Time-lapse Routes
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app import models, auth
from app.services.timelapse_service import timelapse_service

router = APIRouter()


class CreateProjectRequest(BaseModel):
    plant_name: str
    description: Optional[str] = ""


@router.post("/project")
async def create_timelapse_project(
    request: CreateProjectRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new time-lapse project"""
    try:
        result = timelapse_service.create_timelapse_project(
            current_user.id,
            request.plant_name,
            request.description or "",
            db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/project/{project_id}/image")
async def add_image_to_timelapse(
    project_id: int,
    file: UploadFile = File(...),
    analysis_id: Optional[int] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Add image to time-lapse project"""
    try:
        # Verify project ownership
        project = db.query(models.TimeLapseProject).filter(
            models.TimeLapseProject.id == project_id,
            models.TimeLapseProject.user_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        image_data = await file.read()
        result = timelapse_service.add_image_to_timelapse(
            project_id,
            image_data,
            analysis_id,
            db
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/project/{project_id}/progress")
async def get_timelapse_progress(
    project_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get time-lapse progress"""
    try:
        # Verify ownership
        project = db.query(models.TimeLapseProject).filter(
            models.TimeLapseProject.id == project_id,
            models.TimeLapseProject.user_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        result = timelapse_service.get_timelapse_progress(project_id, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/project/{project_id}/generate-video")
async def generate_timelapse_video(
    project_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Generate time-lapse video"""
    try:
        # Verify ownership
        project = db.query(models.TimeLapseProject).filter(
            models.TimeLapseProject.id == project_id,
            models.TimeLapseProject.user_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        result = timelapse_service.generate_timelapse_video(project_id, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/projects")
async def get_user_projects(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user's time-lapse projects"""
    try:
        projects = db.query(models.TimeLapseProject).filter(
            models.TimeLapseProject.user_id == current_user.id
        ).order_by(models.TimeLapseProject.created_at.desc()).all()
        
        return [
            {
                "id": p.id,
                "plant_name": p.plant_name,
                "description": p.description,
                "start_date": p.start_date.isoformat(),
                "created_at": p.created_at.isoformat()
            }
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

