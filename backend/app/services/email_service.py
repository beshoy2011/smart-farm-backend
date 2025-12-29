"""
Enhanced email service with HTML templates
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from typing import Dict, Optional
from datetime import datetime


class EmailService:
    """Service for sending emails with HTML templates"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_USER", "")
        self.password = os.getenv("EMAIL_PASSWORD", "")
        self.enabled = bool(self.email and self.password)
    
    def _send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email with HTML content"""
        if not self.enabled:
            print(f"Email not configured. Would send to {to_email}: {subject}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = to_email
            
            # Add text version if provided
            if text_content:
                part1 = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_weekly_report(
        self, 
        user_email: str, 
        user_name: str, 
        data: Dict
    ) -> bool:
        """Send weekly report email"""
        html_template = """
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
                .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }
                .header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; }
                .header h1 { margin: 0; font-size: 24px; }
                .content { padding: 30px; }
                .greeting { font-size: 18px; color: #333; margin-bottom: 20px; }
                .stat-card { background: #f0f9ff; padding: 20px; margin: 15px 0; border-radius: 8px; border-right: 4px solid #10b981; }
                .stat-card h3 { margin: 0 0 10px 0; color: #10b981; font-size: 18px; }
                .stat-card p { margin: 5px 0; color: #666; font-size: 16px; }
                .stat-value { font-size: 28px; font-weight: bold; color: #059669; }
                .footer { background: #f9fafb; padding: 20px; text-align: center; color: #666; font-size: 14px; }
                .button { display: inline-block; background: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 تقريرك الأسبوعي من SmartFarm AI</h1>
                </div>
                <div class="content">
                    <p class="greeting">مرحباً {{ user_name }},</p>
                    <p>إليك ملخص أسبوعك في SmartFarm AI:</p>
                    
                    <div class="stat-card">
                        <h3>🌱 صحة النباتات</h3>
                        <p class="stat-value">{{ avg_health }}%</p>
                        <p>متوسط صحة النباتات</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3>💧 استخدام المياه</h3>
                        <p class="stat-value">{{ water_used }} لتر</p>
                        <p>المستخدم هذا الأسبوع</p>
                        {% if water_saved > 0 %}
                        <p style="color: #10b981; margin-top: 10px;">✨ وفرت {{ water_saved }} لتر!</p>
                        {% endif %}
                    </div>
                    
                    <div class="stat-card">
                        <h3>📈 التحليلات</h3>
                        <p class="stat-value">{{ total_analyses }}</p>
                        <p>عدد التحليلات هذا الأسبوع</p>
                    </div>
                    
                    {% if achievements|length > 0 %}
                    <div class="stat-card">
                        <h3>🏆 الإنجازات الجديدة</h3>
                        {% for ach in achievements %}
                        <p>{{ ach.icon }} {{ ach.title }} - {{ ach.description }}</p>
                        {% endfor %}
                    </div>
                    {% endif %}
                    
                    <div style="text-align: center;">
                        <a href="https://your-domain.com/dashboard" class="button">عرض التفاصيل الكاملة</a>
                    </div>
                    
                    <p style="margin-top: 30px; color: #666;">شكراً لاستخدامك SmartFarm AI! 🌟</p>
                </div>
                <div class="footer">
                    <p>SmartFarm AI - منصة الزراعة الذكية</p>
                    <p>© 2024 SmartFarm AI. جميع الحقوق محفوظة.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            user_name=user_name or "المستخدم",
            avg_health=data.get('avg_health', 0),
            water_used=data.get('water_used', 0),
            water_saved=data.get('water_saved', 0),
            total_analyses=data.get('total_analyses', 0),
            achievements=data.get('achievements', [])
        )
        
        return self._send_email(
            user_email,
            "📊 تقريرك الأسبوعي - SmartFarm AI",
            html_content
        )
    
    def send_alert_email(
        self,
        user_email: str,
        user_name: str,
        alert_type: str,
        message: str,
        plant_name: Optional[str] = None
    ) -> bool:
        """Send alert email"""
        alert_icons = {
            "water": "💧",
            "disease": "🦠",
            "temperature": "🌡️",
            "fertilizer": "💊"
        }
        
        alert_titles = {
            "water": "تنبيه: نقص المياه",
            "disease": "تنبيه: خطر الإصابة",
            "temperature": "تنبيه: درجة حرارة عالية",
            "fertilizer": "تنبيه: يحتاج سماد"
        }
        
        html_template = """
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
                .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }
                .header { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 30px; text-align: center; }
                .content { padding: 30px; }
                .alert-box { background: #fef2f2; border: 2px solid #ef4444; padding: 20px; border-radius: 8px; margin: 20px 0; }
                .alert-box h2 { color: #dc2626; margin: 0 0 15px 0; }
                .alert-box p { color: #666; font-size: 16px; line-height: 1.6; }
                .button { display: inline-block; background: #ef4444; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{{ icon }} {{ title }}</h1>
                </div>
                <div class="content">
                    <p>مرحباً {{ user_name }},</p>
                    <div class="alert-box">
                        <h2>{{ title }}</h2>
                        <p>{{ message }}</p>
                        {% if plant_name %}
                        <p><strong>النبات:</strong> {{ plant_name }}</p>
                        {% endif %}
                    </div>
                    <div style="text-align: center;">
                        <a href="https://your-domain.com/dashboard" class="button">عرض التفاصيل</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            icon=alert_icons.get(alert_type, "⚠️"),
            title=alert_titles.get(alert_type, "تنبيه"),
            user_name=user_name or "المستخدم",
            message=message,
            plant_name=plant_name
        )
        
        return self._send_email(
            user_email,
            f"⚠️ {alert_titles.get(alert_type, 'تنبيه')} - SmartFarm AI",
            html_content
        )
    
    def send_achievement_email(
        self,
        user_email: str,
        user_name: str,
        achievement: Dict
    ) -> bool:
        """Send achievement unlock email"""
        html_template = """
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
                .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }
                .header { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 30px; text-align: center; }
                .content { padding: 30px; text-align: center; }
                .achievement-icon { font-size: 80px; margin: 20px 0; }
                .achievement-title { font-size: 28px; color: #d97706; margin: 10px 0; }
                .achievement-desc { font-size: 18px; color: #666; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏆 إنجاز جديد!</h1>
                </div>
                <div class="content">
                    <div class="achievement-icon">{{ icon }}</div>
                    <h2 class="achievement-title">{{ title }}</h2>
                    <p class="achievement-desc">{{ description }}</p>
                    <p>مبروك {{ user_name }}! 🎉</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            icon=achievement.get('icon', '🏆'),
            title=achievement.get('title', 'إنجاز جديد'),
            description=achievement.get('description', ''),
            user_name=user_name or "المستخدم"
        )
        
        return self._send_email(
            user_email,
            f"🏆 {achievement.get('title', 'إنجاز جديد')} - SmartFarm AI",
            html_content
        )


