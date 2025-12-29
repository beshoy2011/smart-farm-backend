"""
Daily Recommendations Service
Generates personalized daily recommendations
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta


class DailyRecommendationsService:
    """Service for daily personalized recommendations"""
    
    def generate_daily_recommendations(self, user_id: int, db: Session) -> Dict:
        """
        Generate daily recommendations for user
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Daily recommendations
        """
        today = datetime.utcnow().date()
        
        # Get today's analyses
        today_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= datetime.combine(today, datetime.min.time()),
            models.Analysis.created_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
        ).all()
        
        # Get recent analyses (last 3 days)
        recent_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= datetime.utcnow() - timedelta(days=3)
        ).all()
        
        recommendations = []
        
        # Morning recommendations
        morning_tasks = self._generate_morning_tasks(recent_analyses)
        recommendations.extend(morning_tasks)
        
        # Afternoon recommendations
        afternoon_tasks = self._generate_afternoon_tasks(recent_analyses)
        recommendations.extend(afternoon_tasks)
        
        # Evening recommendations
        evening_tasks = self._generate_evening_tasks(recent_analyses)
        recommendations.extend(evening_tasks)
        
        # Priority tasks
        priority_tasks = self._generate_priority_tasks(recent_analyses)
        
        return {
            "date": today.isoformat(),
            "recommendations": recommendations,
            "priority_tasks": priority_tasks,
            "total_tasks": len(recommendations) + len(priority_tasks),
            "completed_tasks": 0,  # Would track from database
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _generate_morning_tasks(self, analyses: List[models.Analysis]) -> List[Dict]:
        """Generate morning tasks"""
        tasks = []
        
        if not analyses:
            tasks.append({
                "time": "morning",
                "priority": "medium",
                "title_ar": "تحليل نباتاتك",
                "title_en": "Analyze your plants",
                "description_ar": "قم بتحليل نباتاتك في الصباح للحصول على توصيات اليوم",
                "description_en": "Analyze your plants in the morning to get today's recommendations",
                "icon": "🌅"
            })
            return tasks
        
        # Check for low health plants
        low_health = [a for a in analyses if (a.plant_health_score or 0) < 50]
        if low_health:
            tasks.append({
                "time": "morning",
                "priority": "high",
                "title_ar": "فحص النباتات منخفضة الصحة",
                "title_en": "Check low health plants",
                "description_ar": f"لديك {len(low_health)} نبات يحتاج إلى عناية فورية",
                "description_en": f"You have {len(low_health)} plant(s) needing immediate care",
                "icon": "⚠️"
            })
        
        # Check for water needs
        needs_water = [a for a in analyses if (a.water_needs or 0) > 5]
        if needs_water:
            tasks.append({
                "time": "morning",
                "priority": "high",
                "title_ar": "ري النباتات",
                "title_en": "Water plants",
                "description_ar": f"ري {len(needs_water)} نبات في الصباح الباكر",
                "description_en": f"Water {len(needs_water)} plant(s) in early morning",
                "icon": "💧"
            })
        
        return tasks
    
    def _generate_afternoon_tasks(self, analyses: List[models.Analysis]) -> List[Dict]:
        """Generate afternoon tasks"""
        tasks = []
        
        if not analyses:
            return tasks
        
        # Check for diseases
        has_diseases = [a for a in analyses if a.diseases and len(a.diseases) > 0]
        if has_diseases:
            tasks.append({
                "time": "afternoon",
                "priority": "medium",
                "title_ar": "معالجة الأمراض",
                "title_en": "Treat diseases",
                "description_ar": "استخدم مبيدات طبيعية لمعالجة الأمراض المكتشفة",
                "description_en": "Use natural pesticides to treat detected diseases",
                "icon": "🦠"
            })
        
        # Check for pests
        has_pests = [a for a in analyses if a.pests and (isinstance(a.pests, list) and len(a.pests) > 0)]
        if has_pests:
            tasks.append({
                "time": "afternoon",
                "priority": "medium",
                "title_ar": "مكافحة الآفات",
                "title_en": "Control pests",
                "description_ar": "فحص وعلاج الآفات في النباتات",
                "description_en": "Inspect and treat pests in plants",
                "icon": "🐛"
            })
        
        return tasks
    
    def _generate_evening_tasks(self, analyses: List[models.Analysis]) -> List[Dict]:
        """Generate evening tasks"""
        tasks = []
        
        tasks.append({
            "time": "evening",
            "priority": "low",
            "title_ar": "مراجعة اليوم",
            "title_en": "Review today",
            "description_ar": "راجع إنجازات اليوم وتخطيط للغد",
            "description_en": "Review today's achievements and plan for tomorrow",
            "icon": "📝"
        })
        
        if analyses:
            tasks.append({
                "time": "evening",
                "priority": "low",
                "title_ar": "توثيق التقدم",
                "title_en": "Document progress",
                "description_ar": "وثّق تقدم نباتاتك بالصور",
                "description_en": "Document your plants' progress with photos",
                "icon": "📸"
            })
        
        return tasks
    
    def _generate_priority_tasks(self, analyses: List[models.Analysis]) -> List[Dict]:
        """Generate priority tasks"""
        tasks = []
        
        if not analyses:
            return tasks
        
        # Critical health
        critical = [a for a in analyses if (a.plant_health_score or 0) < 40]
        if critical:
            tasks.append({
                "priority": "urgent",
                "title_ar": "🚨 حالة حرجة",
                "title_en": "🚨 Critical condition",
                "description_ar": f"{len(critical)} نبات في حالة حرجة - يحتاج عناية فورية",
                "description_en": f"{len(critical)} plant(s) in critical condition - needs immediate care",
                "action_required": True
            })
        
        # High water needs
        high_water = [a for a in analyses if (a.water_needs or 0) > 8]
        if high_water:
            tasks.append({
                "priority": "high",
                "title_ar": "💧 احتياجات مياه عالية",
                "title_en": "💧 High water needs",
                "description_ar": f"{len(high_water)} نبات يحتاج ري فوري",
                "description_en": f"{len(high_water)} plant(s) need immediate watering",
                "action_required": True
            })
        
        return tasks


# Global service instance
daily_recommendations_service = DailyRecommendationsService()

