"""
Smart Notification Service
Intelligent notification system with multiple channels
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta
import asyncio


class SmartNotificationService:
    """Intelligent notification service with multiple channels"""
    
    def __init__(self):
        self.notification_rules = {
            "critical_health": {
                "threshold": 40,
                "priority": "high",
                "channels": ["push", "email", "sms"],
                "message_ar": "🚨 تنبيه عاجل: صحة النبات منخفضة جداً!",
                "message_en": "🚨 Urgent Alert: Plant health is very low!"
            },
            "water_needed": {
                "threshold": 30,
                "priority": "medium",
                "channels": ["push", "email"],
                "message_ar": "💧 تذكير: النبات يحتاج إلى الري",
                "message_en": "💧 Reminder: Plant needs watering"
            },
            "disease_detected": {
                "threshold": 1,
                "priority": "high",
                "channels": ["push", "email"],
                "message_ar": "🦠 تحذير: تم اكتشاف مرض في النبات",
                "message_en": "🦠 Warning: Disease detected in plant"
            },
            "achievement_unlocked": {
                "threshold": 1,
                "priority": "low",
                "channels": ["push"],
                "message_ar": "🏆 مبروك! لقد حصلت على إنجاز جديد",
                "message_en": "🏆 Congratulations! You unlocked a new achievement"
            },
            "weather_alert": {
                "threshold": 1,
                "priority": "high",
                "channels": ["push", "email"],
                "message_ar": "🌦️ تنبيه طقس: ظروف جوية غير مناسبة",
                "message_en": "🌦️ Weather Alert: Unsuitable weather conditions"
            }
        }
    
    def should_send_notification(self, notification_type: str, value: float, 
                                 last_notification: Optional[datetime] = None) -> bool:
        """
        Determine if notification should be sent
        
        Args:
            notification_type: Type of notification
            value: Current value to check
            last_notification: Last notification time
        
        Returns:
            True if notification should be sent
        """
        if notification_type not in self.notification_rules:
            return False
        
        rule = self.notification_rules[notification_type]
        
        # Check threshold
        if notification_type == "critical_health" and value > rule["threshold"]:
            return False
        if notification_type == "water_needed" and value > rule["threshold"]:
            return False
        
        # Check cooldown period (don't spam)
        if last_notification:
            cooldown_hours = 1 if rule["priority"] == "high" else 6
            if datetime.utcnow() - last_notification < timedelta(hours=cooldown_hours):
                return False
        
        return True
    
    def create_notification(self, user_id: int, notification_type: str, 
                           title: str, message: str, data: Optional[Dict] = None,
                           priority: str = "medium", channels: List[str] = None) -> Dict:
        """
        Create a smart notification
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Additional data
            priority: Notification priority
            channels: Notification channels
        
        Returns:
            Notification data
        """
        if channels is None:
            rule = self.notification_rules.get(notification_type, {})
            channels = rule.get("channels", ["push"])
        
        notification = {
            "user_id": user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "data": data or {},
            "priority": priority,
            "channels": channels,
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        }
        
        return notification
    
    def get_user_notifications(self, user_id: int, limit: int = 20, 
                              unread_only: bool = False) -> List[Dict]:
        """
        Get user notifications
        
        Args:
            user_id: User ID
            limit: Maximum number of notifications
            unread_only: Only unread notifications
        
        Returns:
            List of notifications
        """
        # This would typically query the database
        # For now, return mock data structure
        return []
    
    def mark_as_read(self, user_id: int, notification_id: int):
        """Mark notification as read"""
        # Implementation would update database
        pass
    
    def send_notification(self, notification: Dict, db: Session):
        """
        Send notification through all configured channels
        
        Args:
            notification: Notification data
            db: Database session
        """
        user_id = notification["user_id"]
        channels = notification.get("channels", ["push"])
        
        # Send via WebSocket (push)
        if "push" in channels:
            try:
                from app.routers.websocket import broadcast_alert
                asyncio.create_task(
                    broadcast_alert(
                        user_id,
                        notification["type"],
                        notification["message"]
                    )
                )
            except Exception as e:
                print(f"WebSocket notification error: {e}")
        
        # Send via Email
        if "email" in channels:
            try:
                from app.services.email_service import EmailService
                email_service = EmailService()
                user = db.query(models.User).filter(models.User.id == user_id).first()
                if user:
                    asyncio.create_task(
                        email_service.send_alert_email(
                            user.email,
                            notification["title"],
                            notification["message"]
                        )
                    )
            except Exception as e:
                print(f"Email notification error: {e}")
        
        # Send via SMS (would require SMS service integration)
        if "sms" in channels:
            # SMS integration would go here
            pass


# Global service instance
smart_notification_service = SmartNotificationService()


