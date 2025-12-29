"""
Achievement service for unlocking and tracking user achievements
"""

from sqlalchemy.orm import Session
from app import models
from typing import List, Dict
from datetime import datetime


class AchievementService:
    """Service for managing user achievements"""
    
    # Achievement definitions
    ACHIEVEMENTS = {
        "first_analysis": {
            "title": "🌱 المبتدئ",
            "description": "أول تحليل ناجح!",
            "icon": "🌱",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id
            ).count() >= 1
        },
        "ten_analyses": {
            "title": "🎯 الخبير",
            "description": "10 تحليلات ناجحة!",
            "icon": "🎯",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id
            ).count() >= 10
        },
        "fifty_analyses": {
            "title": "⭐ المحترف",
            "description": "50 تحليل ناجح!",
            "icon": "⭐",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id
            ).count() >= 50
        },
        "hundred_analyses": {
            "title": "🏆 المزارع الذهبي",
            "description": "100 تحليل ناجح!",
            "icon": "🏆",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id
            ).count() >= 100
        },
        "water_saver": {
            "title": "💧 خبير الري",
            "description": "وفرت 100+ لتر ماء!",
            "icon": "💧",
            "condition": lambda user_id, db: sum(
                a.cost_savings or 0 for a in db.query(models.Analysis).filter(
                    models.Analysis.user_id == user_id
                ).all()
            ) >= 100
        },
        "water_master": {
            "title": "🌊 سيد المياه",
            "description": "وفرت 1000+ لتر ماء!",
            "icon": "🌊",
            "condition": lambda user_id, db: sum(
                a.cost_savings or 0 for a in db.query(models.Analysis).filter(
                    models.Analysis.user_id == user_id
                ).all()
            ) >= 1000
        },
        "perfect_health": {
            "title": "✨ الصحة المثالية",
            "description": "نبات بصحة 100%!",
            "icon": "✨",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id,
                models.Analysis.plant_health_score >= 100
            ).count() >= 1
        },
        "disease_detector": {
            "title": "🔬 كاشف الأمراض",
            "description": "اكتشفت 5 أمراض!",
            "icon": "🔬",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id,
                models.Analysis.disease_alert == True
            ).count() >= 5
        },
        "early_bird": {
            "title": "🐦 الطائر المبكر",
            "description": "تحليل في أول 7 أيام!",
            "icon": "🐦",
            "condition": lambda user_id, db: db.query(models.User).filter(
                models.User.id == user_id
            ).first() and (
                datetime.now() - db.query(models.User).filter(
                    models.User.id == user_id
                ).first().created_at
            ).days <= 7
        },
        "weekly_warrior": {
            "title": "⚔️ المحارب الأسبوعي",
            "description": "7 تحليلات في أسبوع واحد!",
            "icon": "⚔️",
            "condition": lambda user_id, db: db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id,
                models.Analysis.created_at >= datetime.now().replace(day=datetime.now().day - 7)
            ).count() >= 7
        }
    }
    
    def check_and_unlock_achievements(
        self, 
        user_id: int, 
        db: Session
    ) -> List[Dict]:
        """
        Check and unlock achievements for user
        Returns list of newly unlocked achievements
        """
        newly_unlocked = []
        
        # Get existing achievements
        existing_achievements = db.query(models.Achievement).filter(
            models.Achievement.user_id == user_id
        ).all()
        unlocked_types = {a.achievement_type for a in existing_achievements}
        
        # Check each achievement
        for achievement_type, achievement_def in self.ACHIEVEMENTS.items():
            if achievement_type in unlocked_types:
                continue  # Already unlocked
            
            # Check condition
            try:
                if achievement_def["condition"](user_id, db):
                    # Unlock achievement
                    new_achievement = models.Achievement(
                        user_id=user_id,
                        achievement_type=achievement_type,
                        title=achievement_def["title"],
                        description=achievement_def["description"],
                        icon=achievement_def["icon"]
                    )
                    db.add(new_achievement)
                    db.flush()
                    
                    newly_unlocked.append({
                        "type": achievement_type,
                        "title": achievement_def["title"],
                        "description": achievement_def["description"],
                        "icon": achievement_def["icon"]
                    })
            except Exception as e:
                print(f"Error checking achievement {achievement_type}: {e}")
                continue
        
        if newly_unlocked:
            db.commit()
        
        return newly_unlocked
    
    def get_user_achievements(self, user_id: int, db: Session) -> List[Dict]:
        """Get all achievements for a user"""
        achievements = db.query(models.Achievement).filter(
            models.Achievement.user_id == user_id
        ).order_by(models.Achievement.unlocked_at.desc()).all()
        
        return [
            {
                "id": a.id,
                "type": a.achievement_type,
                "title": a.title,
                "description": a.description,
                "icon": a.icon,
                "unlocked_at": a.unlocked_at.isoformat() if a.unlocked_at else None
            }
            for a in achievements
        ]
    
    def get_achievement_stats(self, user_id: int, db: Session) -> Dict:
        """Get achievement statistics for user"""
        total_achievements = db.query(models.Achievement).filter(
            models.Achievement.user_id == user_id
        ).count()
        
        total_possible = len(self.ACHIEVEMENTS)
        progress = (total_achievements / total_possible * 100) if total_possible > 0 else 0
        
        return {
            "unlocked": total_achievements,
            "total": total_possible,
            "progress": round(progress, 1)
        }


