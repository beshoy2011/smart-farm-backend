"""
Task Management Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.database import get_db
from app import models, auth
from app.services.task_management_service import task_management_service

router = APIRouter()


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[str] = None
    priority: str = "medium"
    task_type: str = "general"
    related_analysis_id: Optional[int] = None


class UpdateTaskStatusRequest(BaseModel):
    status: str


@router.post("/create")
async def create_task(
    request: CreateTaskRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    try:
        due_date = None
        if request.due_date:
            due_date = datetime.fromisoformat(request.due_date)
        
        result = task_management_service.create_task(
            current_user.id,
            request.title,
            request.description or "",
            due_date,
            request.priority,
            request.task_type,
            request.related_analysis_id,
            db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/list")
async def get_tasks(
    status: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's tasks"""
    try:
        result = task_management_service.get_user_tasks(
            current_user.id, status, db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.put("/{task_id}/status")
async def update_task_status(
    task_id: int,
    request: UpdateTaskStatusRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Update task status"""
    try:
        result = task_management_service.update_task_status(
            task_id, request.status, current_user.id, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/overdue")
async def get_overdue_tasks(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get overdue tasks"""
    try:
        result = task_management_service.get_overdue_tasks(current_user.id, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/today")
async def get_tasks_due_today(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks due today"""
    try:
        result = task_management_service.get_tasks_due_today(current_user.id, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/generate-from-analyses")
async def generate_tasks_from_analyses(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Automatically generate tasks from recent analyses"""
    try:
        result = task_management_service.generate_tasks_from_analyses(
            current_user.id, db
        )
        return {
            "generated_tasks": result,
            "count": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

