"""
Smart Automatic Irrigation Service
Intelligent automatic irrigation system
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta
import asyncio


class SmartIrrigationService:
    """Service for intelligent automatic irrigation"""
    
    def __init__(self):
        self.irrigation_rules = {
            "critical_water": {
                "soil_moisture_threshold": 30,
                "health_threshold": 50,
                "action": "irrigate_immediately",
                "duration_minutes": 30
            },
            "low_water": {
                "soil_moisture_threshold": 40,
                "health_threshold": 60,
                "action": "irrigate_scheduled",
                "duration_minutes": 20
            },
            "normal_water": {
                "soil_moisture_threshold": 50,
                "health_threshold": 70,
                "action": "monitor",
                "duration_minutes": 0
            }
        }
    
    def check_irrigation_needs(self, user_id: int, db: Session) -> Dict:
        """
        Check if irrigation is needed for user's plants
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Irrigation recommendations
        """
        # Get recent analyses
        recent_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        if not recent_analyses:
            return {
                "irrigation_needed": False,
                "message_ar": "لا توجد بيانات حديثة. قم بتحليل نباتاتك أولاً.",
                "message_en": "No recent data. Please analyze your plants first."
            }
        
        # Get weather data
        from app.services.weather_prediction_service import weather_prediction_service
        weather = weather_prediction_service.predict_weather("Cairo,EG", 1)
        next_day_rain = weather["predictions"][0].get("rainfall", 0) if weather.get("predictions") else 0
        
        recommendations = []
        urgent_irrigation = False
        
        for analysis in recent_analyses:
            soil_moisture = analysis.soil_moisture or 50
            health_score = analysis.plant_health_score or 50
            water_needs = analysis.water_needs or 0
            
            # Check if irrigation needed
            if soil_moisture < 30 and health_score < 50:
                urgent_irrigation = True
                recommendations.append({
                    "analysis_id": analysis.id,
                    "priority": "urgent",
                    "action": "irrigate_immediately",
                    "duration_minutes": 30,
                    "reason_ar": f"رطوبة التربة منخفضة ({soil_moisture}%) وصحة النبات حرجة ({health_score}%)",
                    "reason_en": f"Soil moisture low ({soil_moisture}%) and plant health critical ({health_score}%)"
                })
            elif soil_moisture < 40 and next_day_rain < 5:
                recommendations.append({
                    "analysis_id": analysis.id,
                    "priority": "high",
                    "action": "irrigate_scheduled",
                    "duration_minutes": 20,
                    "reason_ar": f"رطوبة التربة منخفضة ({soil_moisture}%) ولا أمطار متوقعة",
                    "reason_en": f"Soil moisture low ({soil_moisture}%) and no rain expected"
                })
            elif water_needs > 5:
                recommendations.append({
                    "analysis_id": analysis.id,
                    "priority": "medium",
                    "action": "monitor_and_irrigate",
                    "duration_minutes": 15,
                    "reason_ar": f"احتياجات المياه عالية ({water_needs} لتر/يوم)",
                    "reason_en": f"High water needs ({water_needs} liters/day)"
                })
        
        return {
            "irrigation_needed": len(recommendations) > 0,
            "urgent": urgent_irrigation,
            "recommendations": recommendations,
            "total_plants": len(recent_analyses),
            "plants_needing_irrigation": len(recommendations),
            "next_rainfall": next_day_rain,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def schedule_irrigation(self, user_id: int, analysis_id: int,
                           duration_minutes: int, scheduled_time: Optional[datetime] = None,
                           db: Session = None) -> Dict:
        """
        Schedule automatic irrigation
        
        Args:
            user_id: User ID
            analysis_id: Analysis ID
            duration_minutes: Irrigation duration in minutes
            scheduled_time: When to irrigate (None = immediate)
            db: Database session
        
        Returns:
            Irrigation schedule data
        """
        if scheduled_time is None:
            scheduled_time = datetime.utcnow()
        
        irrigation_schedule = models.IrrigationSchedule(
            user_id=user_id,
            analysis_id=analysis_id,
            scheduled_time=scheduled_time,
            duration_minutes=duration_minutes,
            status="scheduled"
        )
        db.add(irrigation_schedule)
        db.commit()
        db.refresh(irrigation_schedule)
        
        return {
            "id": irrigation_schedule.id,
            "analysis_id": analysis_id,
            "scheduled_time": scheduled_time.isoformat(),
            "duration_minutes": duration_minutes,
            "status": "scheduled",
            "message_ar": f"تم جدولة الري لمدة {duration_minutes} دقيقة",
            "message_en": f"Irrigation scheduled for {duration_minutes} minutes"
        }
    
    def execute_irrigation(self, schedule_id: int, db: Session) -> Dict:
        """
        Execute irrigation (mock - would control actual irrigation system)
        
        Args:
            schedule_id: Schedule ID
            db: Database session
        
        Returns:
            Execution status
        """
        schedule = db.query(models.IrrigationSchedule).filter(
            models.IrrigationSchedule.id == schedule_id
        ).first()
        
        if not schedule:
            raise ValueError("Schedule not found")
        
        if schedule.status != "scheduled":
            raise ValueError(f"Schedule is {schedule.status}, cannot execute")
        
        # In production, this would:
        # 1. Send command to IoT irrigation device
        # 2. Monitor water flow
        # 3. Stop after duration
        # 4. Log water usage
        
        schedule.status = "executing"
        schedule.started_at = datetime.utcnow()
        db.commit()
        
        # Simulate irrigation completion
        schedule.status = "completed"
        schedule.completed_at = datetime.utcnow()
        schedule.water_used_liters = schedule.duration_minutes * 2  # 2 liters per minute
        db.commit()
        
        return {
            "id": schedule_id,
            "status": "completed",
            "water_used_liters": schedule.water_used_liters,
            "duration_minutes": schedule.duration_minutes,
            "message_ar": f"تم الري بنجاح. استخدم {schedule.water_used_liters} لتر",
            "message_en": f"Irrigation completed. Used {schedule.water_used_liters} liters"
        }
    
    def get_irrigation_history(self, user_id: int, days: int = 30,
                               db: Session = None) -> List[Dict]:
        """
        Get irrigation history
        
        Args:
            user_id: User ID
            days: Number of days to look back
            db: Database session
        
        Returns:
            Irrigation history
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        schedules = db.query(models.IrrigationSchedule).filter(
            models.IrrigationSchedule.user_id == user_id,
            models.IrrigationSchedule.created_at >= cutoff
        ).order_by(models.IrrigationSchedule.created_at.desc()).all()
        
        return [
            {
                "id": s.id,
                "analysis_id": s.analysis_id,
                "scheduled_time": s.scheduled_time.isoformat(),
                "duration_minutes": s.duration_minutes,
                "water_used_liters": s.water_used_liters,
                "status": s.status,
                "created_at": s.created_at.isoformat()
            }
            for s in schedules
        ]
    
    def get_water_usage_stats(self, user_id: int, days: int = 30,
                              db: Session = None) -> Dict:
        """
        Get water usage statistics
        
        Args:
            user_id: User ID
            days: Number of days
            db: Database session
        
        Returns:
            Water usage statistics
        """
        history = self.get_irrigation_history(user_id, days, db)
        
        total_water = sum(h.get("water_used_liters", 0) for h in history)
        total_irrigations = len([h for h in history if h.get("status") == "completed"])
        avg_water_per_irrigation = total_water / total_irrigations if total_irrigations > 0 else 0
        
        return {
            "total_water_liters": round(total_water, 1),
            "total_irrigations": total_irrigations,
            "average_water_per_irrigation": round(avg_water_per_irrigation, 1),
            "period_days": days,
            "daily_average": round(total_water / days, 1) if days > 0 else 0
        }


# Global service instance
smart_irrigation_service = SmartIrrigationService()

