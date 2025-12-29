"""
Time-lapse Growth Tracking Service
Tracks plant growth over time using image analysis
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta
import base64


class TimeLapseService:
    """Service for tracking plant growth over time"""
    
    def create_timelapse_project(self, user_id: int, plant_name: str, 
                                  description: str, db: Session) -> Dict:
        """
        Create a new time-lapse project
        
        Args:
            user_id: User ID
            plant_name: Name of the plant
            description: Project description
            db: Database session
        
        Returns:
            Project data
        """
        project = models.TimeLapseProject(
            user_id=user_id,
            plant_name=plant_name,
            description=description,
            start_date=datetime.utcnow()
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        
        return {
            "id": project.id,
            "plant_name": project.plant_name,
            "description": project.description,
            "start_date": project.start_date.isoformat(),
            "images_count": 0,
            "status": "active"
        }
    
    def add_image_to_timelapse(self, project_id: int, image_data: bytes,
                               analysis_id: Optional[int] = None,
                               db: Session = None) -> Dict:
        """
        Add image to time-lapse project
        
        Args:
            project_id: Project ID
            image_data: Image binary data
            analysis_id: Optional analysis ID
            db: Database session
        
        Returns:
            Image data
        """
        # Save image (in production, use cloud storage)
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        timelapse_image = models.TimeLapseImage(
            project_id=project_id,
            analysis_id=analysis_id,
            image_data=image_base64,
            captured_at=datetime.utcnow()
        )
        db.add(timelapse_image)
        db.commit()
        db.refresh(timelapse_image)
        
        # Calculate growth metrics if analysis exists
        growth_metrics = None
        if analysis_id:
            analysis = db.query(models.Analysis).filter(
                models.Analysis.id == analysis_id
            ).first()
            if analysis:
                growth_metrics = {
                    "health_score": analysis.plant_health_score,
                    "water_needs": analysis.water_needs,
                    "height_estimate": self._estimate_height(analysis)
                }
        
        return {
            "id": timelapse_image.id,
            "project_id": project_id,
            "captured_at": timelapse_image.captured_at.isoformat(),
            "growth_metrics": growth_metrics
        }
    
    def get_timelapse_progress(self, project_id: int, db: Session) -> Dict:
        """
        Get time-lapse progress and statistics
        
        Args:
            project_id: Project ID
            db: Database session
        
        Returns:
            Progress data
        """
        project = db.query(models.TimeLapseProject).filter(
            models.TimeLapseProject.id == project_id
        ).first()
        
        if not project:
            raise ValueError("Project not found")
        
        images = db.query(models.TimeLapseImage).filter(
            models.TimeLapseImage.project_id == project_id
        ).order_by(models.TimeLapseImage.captured_at).all()
        
        if len(images) < 2:
            return {
                "project_id": project_id,
                "images_count": len(images),
                "status": "insufficient_data",
                "message": "Need at least 2 images for time-lapse"
            }
        
        # Calculate growth progression
        first_image = images[0]
        last_image = images[-1]
        
        days_elapsed = (last_image.captured_at - first_image.captured_at).days
        
        # Get health progression
        health_progression = []
        for img in images:
            if img.analysis_id:
                analysis = db.query(models.Analysis).filter(
                    models.Analysis.id == img.analysis_id
                ).first()
                if analysis:
                    health_progression.append({
                        "date": img.captured_at.isoformat(),
                        "health_score": analysis.plant_health_score or 0
                    })
        
        return {
            "project_id": project_id,
            "plant_name": project.plant_name,
            "start_date": project.start_date.isoformat(),
            "images_count": len(images),
            "days_elapsed": days_elapsed,
            "health_progression": health_progression,
            "growth_rate": self._calculate_growth_rate(images, db),
            "status": "active"
        }
    
    def _estimate_height(self, analysis: models.Analysis) -> float:
        """Estimate plant height from analysis"""
        # Simple estimation based on health and water needs
        base_height = 10  # cm
        health_factor = (analysis.plant_health_score or 50) / 100
        return round(base_height * (1 + health_factor), 1)
    
    def _calculate_growth_rate(self, images: List[models.TimeLapseImage], 
                               db: Session) -> Dict:
        """Calculate growth rate from images"""
        if len(images) < 2:
            return {"rate": 0, "trend": "stable"}
        
        # Get health scores
        health_scores = []
        for img in images:
            if img.analysis_id:
                analysis = db.query(models.Analysis).filter(
                    models.Analysis.id == img.analysis_id
                ).first()
                if analysis and analysis.plant_health_score:
                    health_scores.append(analysis.plant_health_score)
        
        if len(health_scores) < 2:
            return {"rate": 0, "trend": "stable"}
        
        # Calculate average change
        first_avg = sum(health_scores[:len(health_scores)//2]) / (len(health_scores)//2)
        second_avg = sum(health_scores[len(health_scores)//2:]) / (len(health_scores) - len(health_scores)//2)
        
        change = second_avg - first_avg
        
        if change > 5:
            trend = "growing"
        elif change < -5:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "rate": round(change, 2),
            "trend": trend,
            "percentage_change": round((change / first_avg) * 100, 1) if first_avg > 0 else 0
        }
    
    def generate_timelapse_video(self, project_id: int, db: Session) -> Dict:
        """
        Generate time-lapse video (mock - would use video processing in production)
        
        Args:
            project_id: Project ID
            db: Database session
        
        Returns:
            Video generation status
        """
        images = db.query(models.TimeLapseImage).filter(
            models.TimeLapseImage.project_id == project_id
        ).order_by(models.TimeLapseImage.captured_at).all()
        
        if len(images) < 5:
            return {
                "status": "insufficient_images",
                "message": "Need at least 5 images to generate video",
                "required": 5,
                "current": len(images)
            }
        
        # In production, this would:
        # 1. Download all images
        # 2. Process them into video frames
        # 3. Generate video file
        # 4. Upload to storage
        # 5. Return video URL
        
        return {
            "status": "processing",
            "message": "Video generation started",
            "images_count": len(images),
            "estimated_duration": f"{len(images) * 0.5:.1f} seconds",
            "video_url": f"/api/timelapse/{project_id}/video"  # Mock URL
        }


# Global service instance
timelapse_service = TimeLapseService()

