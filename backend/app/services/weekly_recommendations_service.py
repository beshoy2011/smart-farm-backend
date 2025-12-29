"""
Weekly Recommendations Service
Generates intelligent weekly recommendations for users
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta


class WeeklyRecommendationsService:
    """Service for generating weekly agricultural recommendations"""
    
    def generate_recommendations(self, user_id: int, db: Session) -> Dict:
        """
        Generate weekly recommendations for user
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Weekly recommendations
        """
        # Get user's recent analyses
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= week_ago
        ).all()
        
        if not recent_analyses:
            return {
                "message_ar": "لا توجد تحليلات حديثة. قم بتحليل نباتاتك للحصول على توصيات مخصصة.",
                "message_en": "No recent analyses. Analyze your plants to get personalized recommendations.",
                "recommendations": []
            }
        
        # Analyze trends
        avg_health = sum(a.plant_health_score or 0 for a in recent_analyses) / len(recent_analyses)
        avg_water = sum(a.water_needs or 0 for a in recent_analyses) / len(recent_analyses)
        
        total_diseases = sum(len(a.diseases or []) for a in recent_analyses)
        total_pests = sum(len(a.pests or []) if isinstance(a.pests, list) else 0 for a in recent_analyses)
        
        recommendations = []
        
        # Health-based recommendations
        if avg_health < 50:
            recommendations.append({
                "priority": "high",
                "category": "health",
                "title_ar": "تحسين صحة النبات",
                "title_en": "Improve Plant Health",
                "message_ar": f"متوسط صحة النباتات {avg_health:.1f}%. راجع نظام الري والتسميد.",
                "message_en": f"Average plant health is {avg_health:.1f}%. Review irrigation and fertilization.",
                "actions": [
                    "زيادة الري إذا كانت التربة جافة",
                    "استخدام أسمدة عضوية",
                    "فحص النباتات يومياً"
                ]
            })
        
        # Water recommendations
        if avg_water > 5:
            recommendations.append({
                "priority": "medium",
                "category": "water",
                "title_ar": "إدارة المياه",
                "title_en": "Water Management",
                "message_ar": f"متوسط احتياجات المياه {avg_water:.1f} لتر/يوم. استخدم نظام الري بالتنقيط.",
                "message_en": f"Average water needs {avg_water:.1f} liters/day. Use drip irrigation.",
                "actions": [
                    "تثبيت نظام ري بالتنقيط",
                    "ري في الصباح الباكر",
                    "استخدام المهاد (mulch) للاحتفاظ بالرطوبة"
                ]
            })
        
        # Disease recommendations
        if total_diseases > 0:
            recommendations.append({
                "priority": "high",
                "category": "disease",
                "title_ar": "مكافحة الأمراض",
                "title_en": "Disease Control",
                "message_ar": f"تم اكتشاف {total_diseases} مرض(ات). استخدم مبيدات طبيعية.",
                "message_en": f"{total_diseases} disease(s) detected. Use natural pesticides.",
                "actions": [
                    "استخدام زيت النيم",
                    "تحسين التهوية",
                    "عزل النباتات المصابة"
                ]
            })
        
        # Pest recommendations
        if total_pests > 0:
            recommendations.append({
                "priority": "medium",
                "category": "pest",
                "title_ar": "مكافحة الآفات",
                "title_en": "Pest Control",
                "message_ar": f"تم اكتشاف {total_pests} آفة(ات). شجع الحشرات المفيدة.",
                "message_en": f"{total_pests} pest(s) detected. Encourage beneficial insects.",
                "actions": [
                    "زراعة نباتات تجذب الحشرات المفيدة",
                    "استخدام صابون مبيد للحشرات",
                    "فحص الأوراق بانتظام"
                ]
            })
        
        # General recommendations
        if avg_health >= 70:
            recommendations.append({
                "priority": "low",
                "category": "general",
                "title_ar": "حالة ممتازة",
                "title_en": "Excellent Condition",
                "message_ar": "نباتاتك في حالة ممتازة! استمر في العناية بها.",
                "message_en": "Your plants are in excellent condition! Keep up the good work.",
                "actions": [
                    "الاستمرار في المتابعة اليومية",
                    "توثيق التقدم",
                    "مشاركة النتائج"
                ]
            })
        
        # Calculate weekly stats
        stats = {
            "analyses_count": len(recent_analyses),
            "average_health": round(avg_health, 1),
            "average_water_needs": round(avg_water, 1),
            "diseases_detected": total_diseases,
            "pests_detected": total_pests,
            "improvement_rate": self._calculate_improvement_rate(recent_analyses)
        }
        
        return {
            "week_start": week_ago.isoformat(),
            "week_end": datetime.utcnow().isoformat(),
            "stats": stats,
            "recommendations": recommendations,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _calculate_improvement_rate(self, analyses: List[models.Analysis]) -> float:
        """Calculate improvement rate over time"""
        if len(analyses) < 2:
            return 0.0
        
        sorted_analyses = sorted(analyses, key=lambda x: x.created_at)
        first_health = sorted_analyses[0].plant_health_score or 0
        last_health = sorted_analyses[-1].plant_health_score or 0
        
        if first_health == 0:
            return 0.0
        
        improvement = ((last_health - first_health) / first_health) * 100
        return round(improvement, 1)
    
    def save_recommendations(self, user_id: int, recommendations: Dict, db: Session):
        """Save recommendations to database"""
        week_start = datetime.fromisoformat(recommendations["week_start"].replace('Z', '+00:00'))
        
        # Check if recommendations already exist for this week
        existing = db.query(models.WeeklyRecommendation).filter(
            models.WeeklyRecommendation.user_id == user_id,
            models.WeeklyRecommendation.week_start_date >= week_start - timedelta(days=1),
            models.WeeklyRecommendation.week_start_date <= week_start + timedelta(days=1)
        ).first()
        
        if existing:
            existing.recommendations = recommendations
            existing.plant_ids = [a.id for a in db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id,
                models.Analysis.created_at >= week_start
            ).all()]
        else:
            new_recommendation = models.WeeklyRecommendation(
                user_id=user_id,
                week_start_date=week_start,
                recommendations=recommendations,
                plant_ids=[a.id for a in db.query(models.Analysis).filter(
                    models.Analysis.user_id == user_id,
                    models.Analysis.created_at >= week_start
                ).all()]
            )
            db.add(new_recommendation)
        
        db.commit()


# Global service instance
weekly_recommendations_service = WeeklyRecommendationsService()


