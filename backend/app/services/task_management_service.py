"""
Task Management Service
Manages agricultural tasks and reminders
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta


class TaskManagementService:
    """Service for managing agricultural tasks"""
    
    def create_task(self, user_id: int, title: str, description: str,
                   due_date: Optional[datetime] = None, priority: str = "medium",
                   task_type: str = "general", related_analysis_id: Optional[int] = None,
                   db: Session = None) -> Dict:
        """
        Create a new task
        
        Args:
            user_id: User ID
            title: Task title
            description: Task description
            due_date: Due date
            priority: Priority (low, medium, high, urgent)
            task_type: Task type (watering, fertilizing, pruning, etc.)
            related_analysis_id: Related analysis ID
            db: Database session
        
        Returns:
            Task data
        """
        task = models.AgriculturalTask(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            task_type=task_type,
            related_analysis_id=related_analysis_id,
            status="pending"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "task_type": task.task_type,
            "status": task.status,
            "created_at": task.created_at.isoformat()
        }
    
    def get_user_tasks(self, user_id: int, status: Optional[str] = None,
                      db: Session = None) -> List[Dict]:
        """
        Get user's tasks
        
        Args:
            user_id: User ID
            status: Filter by status (pending, in_progress, completed, cancelled)
            db: Database session
        
        Returns:
            List of tasks
        """
        query = db.query(models.AgriculturalTask).filter(
            models.AgriculturalTask.user_id == user_id
        )
        
        if status:
            query = query.filter(models.AgriculturalTask.status == status)
        
        tasks = query.order_by(
            models.AgriculturalTask.priority.desc(),
            models.AgriculturalTask.due_date.asc()
        ).all()
        
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "priority": t.priority,
                "task_type": t.task_type,
                "status": t.status,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
                "created_at": t.created_at.isoformat()
            }
            for t in tasks
        ]
    
    def update_task_status(self, task_id: int, status: str, user_id: int,
                          db: Session = None) -> Dict:
        """
        Update task status
        
        Args:
            task_id: Task ID
            status: New status
            user_id: User ID (for verification)
            db: Database session
        
        Returns:
            Updated task data
        """
        task = db.query(models.AgriculturalTask).filter(
            models.AgriculturalTask.id == task_id,
            models.AgriculturalTask.user_id == user_id
        ).first()
        
        if not task:
            raise ValueError("Task not found")
        
        task.status = status
        if status == "completed":
            task.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(task)
        
        return {
            "id": task.id,
            "status": task.status,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
    
    def get_overdue_tasks(self, user_id: int, db: Session = None) -> List[Dict]:
        """Get overdue tasks"""
        now = datetime.utcnow()
        
        tasks = db.query(models.AgriculturalTask).filter(
            models.AgriculturalTask.user_id == user_id,
            models.AgriculturalTask.status.in_(["pending", "in_progress"]),
            models.AgriculturalTask.due_date < now
        ).all()
        
        return [
            {
                "id": t.id,
                "title": t.title,
                "due_date": t.due_date.isoformat(),
                "days_overdue": (now - t.due_date).days
            }
            for t in tasks
        ]
    
    def get_tasks_due_today(self, user_id: int, db: Session = None) -> List[Dict]:
        """Get tasks due today"""
        today_start = datetime.combine(datetime.utcnow().date(), datetime.min.time())
        today_end = datetime.combine(datetime.utcnow().date(), datetime.max.time())
        
        tasks = db.query(models.AgriculturalTask).filter(
            models.AgriculturalTask.user_id == user_id,
            models.AgriculturalTask.status.in_(["pending", "in_progress"]),
            models.AgriculturalTask.due_date >= today_start,
            models.AgriculturalTask.due_date <= today_end
        ).all()
        
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "priority": t.priority,
                "task_type": t.task_type
            }
            for t in tasks
        ]
    
    def generate_tasks_from_analyses(self, user_id: int, db: Session = None) -> List[Dict]:
        """
        Automatically generate tasks from recent analyses
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            List of generated tasks
        """
        recent_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        generated_tasks = []
        
        for analysis in recent_analyses:
            # Watering task
            if (analysis.water_needs or 0) > 5:
                task = self.create_task(
                    user_id,
                    f"ري نبات - {analysis.plant_type or 'غير محدد'}",
                    f"النبات يحتاج {analysis.water_needs:.1f} لتر من الماء",
                    due_date=datetime.utcnow() + timedelta(days=1),
                    priority="high",
                    task_type="watering",
                    related_analysis_id=analysis.id,
                    db=db
                )
                generated_tasks.append(task)
            
            # Disease treatment task
            if analysis.diseases and len(analysis.diseases) > 0:
                task = self.create_task(
                    user_id,
                    f"معالجة أمراض - {analysis.plant_type or 'غير محدد'}",
                    f"تم اكتشاف {len(analysis.diseases)} مرض(ات)",
                    due_date=datetime.utcnow() + timedelta(days=2),
                    priority="high",
                    task_type="disease_treatment",
                    related_analysis_id=analysis.id,
                    db=db
                )
                generated_tasks.append(task)
            
            # Fertilizer task
            if (analysis.fertilizer_need_percent or 0) > 50:
                task = self.create_task(
                    user_id,
                    f"تسميد - {analysis.plant_type or 'غير محدد'}",
                    f"النبات يحتاج {analysis.recommended_fertilizer_amount or 0:.1f} كجم من السماد",
                    due_date=datetime.utcnow() + timedelta(days=3),
                    priority="medium",
                    task_type="fertilizing",
                    related_analysis_id=analysis.id,
                    db=db
                )
                generated_tasks.append(task)
        
        return generated_tasks


# Global service instance
task_management_service = TaskManagementService()

