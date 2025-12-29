"""
Advanced Analytics Service
Comprehensive analytics and insights
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta
from collections import defaultdict


class AdvancedAnalyticsService:
    """Service for advanced analytics and insights"""
    
    def get_comprehensive_stats(self, user_id: int, days: int = 30,
                               db: Session = None) -> Dict:
        """
        Get comprehensive statistics for user
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            db: Database session
        
        Returns:
            Comprehensive statistics
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        # Get all analyses
        analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= cutoff
        ).all()
        
        if not analyses:
            return {
                "message_ar": "لا توجد بيانات للتحليل",
                "message_en": "No data available for analysis"
            }
        
        # Calculate statistics
        health_scores = [a.plant_health_score or 0 for a in analyses]
        water_needs = [a.water_needs or 0 for a in analyses]
        
        # Plant types distribution
        plant_types = defaultdict(int)
        for a in analyses:
            plant_types[a.plant_type or "unknown"] += 1
        
        # Disease statistics
        total_diseases = sum(len(a.diseases or []) for a in analyses)
        disease_types = defaultdict(int)
        for a in analyses:
            if a.diseases:
                for disease in a.diseases:
                    disease_types[disease] += 1
        
        # Pest statistics
        total_pests = sum(len(a.pests or []) if isinstance(a.pests, list) else 0 for a in analyses)
        
        # Time-based trends
        daily_stats = defaultdict(lambda: {"count": 0, "health_sum": 0, "water_sum": 0})
        for a in analyses:
            date_key = a.created_at.date().isoformat()
            daily_stats[date_key]["count"] += 1
            daily_stats[date_key]["health_sum"] += a.plant_health_score or 0
            daily_stats[date_key]["water_sum"] += a.water_needs or 0
        
        daily_trends = [
            {
                "date": date,
                "analyses_count": stats["count"],
                "avg_health": round(stats["health_sum"] / stats["count"], 1) if stats["count"] > 0 else 0,
                "avg_water": round(stats["water_sum"] / stats["count"], 1) if stats["count"] > 0 else 0
            }
            for date, stats in sorted(daily_stats.items())
        ]
        
        return {
            "period": {
                "start": cutoff.isoformat(),
                "end": datetime.utcnow().isoformat(),
                "days": days
            },
            "overview": {
                "total_analyses": len(analyses),
                "avg_health_score": round(sum(health_scores) / len(health_scores), 1) if health_scores else 0,
                "avg_water_needs": round(sum(water_needs) / len(water_needs), 1) if water_needs else 0,
                "min_health": min(health_scores) if health_scores else 0,
                "max_health": max(health_scores) if health_scores else 0
            },
            "plant_types": dict(plant_types),
            "diseases": {
                "total_detected": total_diseases,
                "types": dict(disease_types),
                "most_common": max(disease_types.items(), key=lambda x: x[1])[0] if disease_types else None
            },
            "pests": {
                "total_detected": total_pests
            },
            "trends": {
                "daily": daily_trends,
                "health_trend": self._calculate_trend(health_scores),
                "water_trend": self._calculate_trend(water_needs)
            },
            "insights": self._generate_insights(analyses, health_scores, water_needs, total_diseases, total_pests)
        }
    
    def _calculate_trend(self, values: List[float]) -> Dict:
        """Calculate trend from values"""
        if len(values) < 2:
            return {"direction": "stable", "change": 0}
        
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half) if first_half else 0
        second_avg = sum(second_half) / len(second_half) if second_half else 0
        
        change = second_avg - first_avg
        percentage_change = (change / first_avg * 100) if first_avg > 0 else 0
        
        if change > 0:
            direction = "improving"
        elif change < 0:
            direction = "declining"
        else:
            direction = "stable"
        
        return {
            "direction": direction,
            "change": round(change, 2),
            "percentage_change": round(percentage_change, 1)
        }
    
    def _generate_insights(self, analyses: List[models.Analysis],
                          health_scores: List[float], water_needs: List[float],
                          total_diseases: int, total_pests: int) -> List[Dict]:
        """Generate insights from data"""
        insights = []
        
        avg_health = sum(health_scores) / len(health_scores) if health_scores else 0
        
        if avg_health > 80:
            insights.append({
                "type": "positive",
                "priority": "low",
                "message_ar": "🎉 ممتاز! نباتاتك في حالة صحية ممتازة",
                "message_en": "🎉 Excellent! Your plants are in great health"
            })
        elif avg_health < 50:
            insights.append({
                "type": "warning",
                "priority": "high",
                "message_ar": "⚠️ انتبه! صحة النباتات منخفضة. راجع نظام العناية",
                "message_en": "⚠️ Warning! Plant health is low. Review care system"
            })
        
        if total_diseases > len(analyses) * 0.3:
            insights.append({
                "type": "negative",
                "priority": "high",
                "message_ar": f"🦠 تم اكتشاف {total_diseases} مرض. استخدم مبيدات طبيعية",
                "message_en": f"🦠 {total_diseases} diseases detected. Use natural pesticides"
            })
        
        if total_pests > len(analyses) * 0.2:
            insights.append({
                "type": "negative",
                "priority": "medium",
                "message_ar": f"🐛 تم اكتشاف {total_pests} آفة. راجع نظام المكافحة",
                "message_en": f"🐛 {total_pests} pests detected. Review control system"
            })
        
        avg_water = sum(water_needs) / len(water_needs) if water_needs else 0
        if avg_water > 8:
            insights.append({
                "type": "info",
                "priority": "medium",
                "message_ar": f"💧 احتياجات المياه عالية ({avg_water:.1f} لتر/يوم). استخدم نظام ري فعال",
                "message_en": f"💧 High water needs ({avg_water:.1f} liters/day). Use efficient irrigation"
            })
        
        return insights
    
    def get_comparison_with_others(self, user_id: int, db: Session) -> Dict:
        """
        Compare user's performance with others (anonymized)
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Comparison data
        """
        # Get user's stats
        user_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id
        ).all()
        
        if not user_analyses:
            return {
                "message_ar": "لا توجد بيانات للمقارنة",
                "message_en": "No data available for comparison"
            }
        
        user_avg_health = sum(a.plant_health_score or 0 for a in user_analyses) / len(user_analyses)
        
        # Get all users' stats (anonymized)
        all_analyses = db.query(models.Analysis).all()
        all_health_scores = [a.plant_health_score or 0 for a in all_analyses if a.plant_health_score]
        
        if not all_health_scores:
            return {
                "message_ar": "لا توجد بيانات للمقارنة",
                "message_en": "No data available for comparison"
            }
        
        avg_all = sum(all_health_scores) / len(all_health_scores)
        percentile = sum(1 for score in all_health_scores if score < user_avg_health) / len(all_health_scores) * 100
        
        return {
            "user_stats": {
                "avg_health": round(user_avg_health, 1),
                "total_analyses": len(user_analyses)
            },
            "community_stats": {
                "avg_health": round(avg_all, 1),
                "total_analyses": len(all_analyses)
            },
            "comparison": {
                "difference": round(user_avg_health - avg_all, 1),
                "percentile": round(percentile, 1),
                "status": "above_average" if user_avg_health > avg_all else "below_average" if user_avg_health < avg_all else "average"
            }
        }
    
    def get_predictions(self, user_id: int, days_ahead: int = 7,
                       db: Session = None) -> Dict:
        """
        Predict future plant health and needs
        
        Args:
            user_id: User ID
            days_ahead: Days to predict ahead
            db: Database session
        
        Returns:
            Predictions
        """
        # Get recent analyses
        recent_analyses = db.query(models.Analysis).filter(
            models.Analysis.user_id == user_id,
            models.Analysis.created_at >= datetime.utcnow() - timedelta(days=30)
        ).order_by(models.Analysis.created_at).all()
        
        if len(recent_analyses) < 3:
            return {
                "message_ar": "تحتاج إلى 3 تحليلات على الأقل للتنبؤ",
                "message_en": "Need at least 3 analyses for prediction"
            }
        
        # Simple linear prediction
        health_scores = [a.plant_health_score or 0 for a in recent_analyses[-5:]]
        if len(health_scores) >= 2:
            trend = (health_scores[-1] - health_scores[0]) / len(health_scores)
            predicted_health = health_scores[-1] + (trend * days_ahead)
            predicted_health = max(0, min(100, predicted_health))  # Clamp to 0-100
        else:
            predicted_health = health_scores[-1] if health_scores else 50
        
        return {
            "current_health": round(health_scores[-1], 1) if health_scores else 0,
            "predicted_health": round(predicted_health, 1),
            "days_ahead": days_ahead,
            "confidence": "medium",
            "recommendations": self._get_prediction_recommendations(predicted_health, health_scores[-1] if health_scores else 0)
        }
    
    def _get_prediction_recommendations(self, predicted_health: float,
                                       current_health: float) -> List[str]:
        """Get recommendations based on predictions"""
        recommendations = []
        
        if predicted_health < current_health:
            recommendations.append("⚠️ صحة النبات متوقعة للتراجع. زد العناية")
        elif predicted_health > current_health:
            recommendations.append("✅ صحة النبات متوقعة للتحسن. استمر في العناية")
        
        if predicted_health < 50:
            recommendations.append("🔍 راقب النباتات يومياً")
            recommendations.append("💧 تأكد من نظام الري")
        
        return recommendations


# Global service instance
advanced_analytics_service = AdvancedAnalyticsService()

