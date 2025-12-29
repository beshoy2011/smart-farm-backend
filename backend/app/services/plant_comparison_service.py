"""
Advanced Plant Comparison Service
Compares plants over time using AI analysis
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta


class PlantComparisonService:
    """Service for comparing plant health over time"""
    
    def compare_plants(self, analysis_id_1: int, analysis_id_2: int, db: Session) -> Dict:
        """
        Compare two plant analyses
        
        Args:
            analysis_id_1: First analysis ID
            analysis_id_2: Second analysis ID
            db: Database session
        
        Returns:
            Comparison results
        """
        analysis1 = db.query(models.Analysis).filter(models.Analysis.id == analysis_id_1).first()
        analysis2 = db.query(models.Analysis).filter(models.Analysis.id == analysis_id_2).first()
        
        if not analysis1 or not analysis2:
            raise ValueError("One or both analyses not found")
        
        if analysis1.user_id != analysis2.user_id:
            raise ValueError("Analyses must belong to the same user")
        
        # Calculate improvements/declines
        health_change = (analysis2.plant_health_score or 0) - (analysis1.plant_health_score or 0)
        water_change = (analysis2.water_needs or 0) - (analysis1.water_needs or 0)
        time_diff = (analysis2.created_at - analysis1.created_at).days
        
        # Determine status
        if health_change > 10:
            status = "improved"
            status_ar = "تحسن"
            status_en = "Improved"
            icon = "📈"
        elif health_change < -10:
            status = "declined"
            status_ar = "تراجع"
            status_en = "Declined"
            icon = "📉"
        else:
            status = "stable"
            status_ar = "مستقر"
            status_en = "Stable"
            icon = "➡️"
        
        # Generate insights
        insights = []
        
        if health_change > 0:
            insights.append({
                "type": "positive",
                "message_ar": f"✅ صحة النبات تحسنت بنسبة {abs(health_change):.1f}% خلال {time_diff} يوم",
                "message_en": f"✅ Plant health improved by {abs(health_change):.1f}% over {time_diff} days"
            })
        elif health_change < 0:
            insights.append({
                "type": "negative",
                "message_ar": f"⚠️ صحة النبات تراجعت بنسبة {abs(health_change):.1f}% خلال {time_diff} يوم",
                "message_en": f"⚠️ Plant health declined by {abs(health_change):.1f}% over {time_diff} days"
            })
        
        if water_change > 0:
            insights.append({
                "type": "info",
                "message_ar": f"💧 احتياجات المياه زادت بمقدار {water_change:.1f} لتر/يوم",
                "message_en": f"💧 Water needs increased by {water_change:.1f} liters/day"
            })
        elif water_change < 0:
            insights.append({
                "type": "info",
                "message_ar": f"💧 احتياجات المياه انخفضت بمقدار {abs(water_change):.1f} لتر/يوم",
                "message_en": f"💧 Water needs decreased by {abs(water_change):.1f} liters/day"
            })
        
        # Compare diseases
        diseases1 = analysis1.diseases or []
        diseases2 = analysis2.diseases or []
        
        if len(diseases2) < len(diseases1):
            insights.append({
                "type": "positive",
                "message_ar": f"🦠 عدد الأمراض انخفض من {len(diseases1)} إلى {len(diseases2)}",
                "message_en": f"🦠 Number of diseases decreased from {len(diseases1)} to {len(diseases2)}"
            })
        elif len(diseases2) > len(diseases1):
            insights.append({
                "type": "negative",
                "message_ar": f"🦠 عدد الأمراض زاد من {len(diseases1)} إلى {len(diseases2)}",
                "message_en": f"🦠 Number of diseases increased from {len(diseases1)} to {len(diseases2)}"
            })
        
        return {
            "analysis_1": {
                "id": analysis1.id,
                "health_score": analysis1.plant_health_score,
                "water_needs": analysis1.water_needs,
                "date": analysis1.created_at.isoformat(),
                "diseases_count": len(diseases1)
            },
            "analysis_2": {
                "id": analysis2.id,
                "health_score": analysis2.plant_health_score,
                "water_needs": analysis2.water_needs,
                "date": analysis2.created_at.isoformat(),
                "diseases_count": len(diseases2)
            },
            "comparison": {
                "health_change": round(health_change, 2),
                "water_change": round(water_change, 2),
                "time_difference_days": time_diff,
                "status": status,
                "status_ar": status_ar,
                "status_en": status_en,
                "icon": icon
            },
            "insights": insights,
            "recommendations": self._generate_recommendations(health_change, water_change, diseases1, diseases2)
        }
    
    def _generate_recommendations(self, health_change: float, water_change: float, 
                                  diseases1: List, diseases2: List) -> List[Dict]:
        """Generate recommendations based on comparison"""
        recommendations = []
        
        if health_change < -10:
            recommendations.append({
                "priority": "high",
                "message_ar": "🔍 صحة النبات في تراجع. راجع نظام الري والتسميد.",
                "message_en": "🔍 Plant health is declining. Review irrigation and fertilization."
            })
        
        if len(diseases2) > len(diseases1):
            recommendations.append({
                "priority": "high",
                "message_ar": "🦠 الأمراض في ازدياد. استخدم مبيدات طبيعية.",
                "message_en": "🦠 Diseases are increasing. Use natural pesticides."
            })
        
        if water_change > 5:
            recommendations.append({
                "priority": "medium",
                "message_ar": "💧 احتياجات المياه زادت. تأكد من نظام الري.",
                "message_en": "💧 Water needs increased. Ensure irrigation system."
            })
        
        if health_change > 10:
            recommendations.append({
                "priority": "low",
                "message_ar": "✅ النبات في حالة جيدة! استمر في العناية به.",
                "message_en": "✅ Plant is in good condition! Continue caring for it."
            })
        
        return recommendations
    
    def get_timeline_comparison(self, user_id: int, plant_type: Optional[str] = None, 
                                days: int = 30, db: Session = None) -> Dict:
        """
        Compare plants over a timeline
        
        Args:
            user_id: User ID
            plant_type: Optional plant type filter
            days: Number of days to look back
            db: Database session
        
        Returns:
            Timeline comparison data
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= cutoff_date
        )
        
        if plant_type:
            query = query.filter(models.Analysis.plant_type == plant_type)
        
        analyses = query.order_by(models.Analysis.created_at).all()
        
        if len(analyses) < 2:
            return {
                "message_ar": "لا توجد تحليلات كافية للمقارنة",
                "message_en": "Not enough analyses for comparison",
                "analyses_count": len(analyses)
            }
        
        # Calculate trends
        health_scores = [a.plant_health_score or 0 for a in analyses]
        avg_health = sum(health_scores) / len(health_scores) if health_scores else 0
        
        first_health = health_scores[0]
        last_health = health_scores[-1]
        overall_change = last_health - first_health
        
        return {
            "analyses_count": len(analyses),
            "time_period_days": days,
            "first_analysis": {
                "id": analyses[0].id,
                "health_score": first_health,
                "date": analyses[0].created_at.isoformat()
            },
            "last_analysis": {
                "id": analyses[-1].id,
                "health_score": last_health,
                "date": analyses[-1].created_at.isoformat()
            },
            "trends": {
                "average_health": round(avg_health, 2),
                "overall_change": round(overall_change, 2),
                "trend": "improving" if overall_change > 5 else "declining" if overall_change < -5 else "stable"
            },
            "timeline": [
                {
                    "id": a.id,
                    "health_score": a.plant_health_score or 0,
                    "date": a.created_at.isoformat()
                }
                for a in analyses
            ]
        }


# Global service instance
plant_comparison_service = PlantComparisonService()


