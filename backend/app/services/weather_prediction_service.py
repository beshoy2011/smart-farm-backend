"""
Advanced Weather Prediction Service
Provides intelligent weather forecasts and agricultural alerts
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random


class WeatherPredictionService:
    """Advanced weather prediction and agricultural alerts"""
    
    def __init__(self):
        self.alert_thresholds = {
            "frost": {"temp": 0, "risk": "high"},
            "heat_wave": {"temp": 35, "risk": "high"},
            "drought": {"rainfall": 0, "days": 7, "risk": "medium"},
            "heavy_rain": {"rainfall": 50, "risk": "high"},
            "wind_storm": {"wind_speed": 25, "risk": "high"}
        }
    
    def predict_weather(self, location: str, days: int = 7) -> Dict:
        """
        Predict weather for next N days
        
        Args:
            location: Location name
            days: Number of days to predict
        
        Returns:
            Weather prediction data
        """
        predictions = []
        base_temp = random.uniform(20, 30)
        base_humidity = random.uniform(40, 70)
        base_rainfall = random.uniform(0, 10)
        
        for i in range(days):
            date = datetime.utcnow() + timedelta(days=i)
            
            # Simulate weather variations
            temp = base_temp + random.uniform(-5, 5)
            humidity = max(30, min(90, base_humidity + random.uniform(-10, 10)))
            rainfall = max(0, base_rainfall + random.uniform(-5, 5))
            wind_speed = random.uniform(5, 20)
            
            # Determine weather condition
            if rainfall > 20:
                condition = "rainy"
                icon = "🌧️"
            elif temp > 30:
                condition = "sunny"
                icon = "☀️"
            elif temp < 10:
                condition = "cold"
                icon = "❄️"
            else:
                condition = "partly_cloudy"
                icon = "⛅"
            
            predictions.append({
                "date": date.isoformat(),
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1),
                "rainfall": round(rainfall, 1),
                "wind_speed": round(wind_speed, 1),
                "condition": condition,
                "icon": icon
            })
        
        return {
            "location": location,
            "predictions": predictions,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_agricultural_alerts(self, weather_data: Dict) -> List[Dict]:
        """
        Generate agricultural alerts based on weather predictions
        
        Args:
            weather_data: Weather prediction data
        
        Returns:
            List of alerts
        """
        alerts = []
        
        for prediction in weather_data.get("predictions", []):
            temp = prediction.get("temperature", 20)
            rainfall = prediction.get("rainfall", 0)
            wind_speed = prediction.get("wind_speed", 10)
            date = prediction.get("date")
            
            # Frost alert
            if temp < self.alert_thresholds["frost"]["temp"]:
                alerts.append({
                    "type": "frost",
                    "severity": "high",
                    "message_ar": f"⚠️ تحذير: صقيع متوقع في {date[:10]}. غطِ النباتات الحساسة!",
                    "message_en": f"⚠️ Warning: Frost expected on {date[:10]}. Cover sensitive plants!",
                    "date": date,
                    "icon": "❄️"
                })
            
            # Heat wave alert
            if temp > self.alert_thresholds["heat_wave"]["temp"]:
                alerts.append({
                    "type": "heat_wave",
                    "severity": "high",
                    "message_ar": f"🌡️ تحذير: موجة حر في {date[:10]}. زد الري!",
                    "message_en": f"🌡️ Warning: Heat wave on {date[:10]}. Increase watering!",
                    "date": date,
                    "icon": "🌡️"
                })
            
            # Heavy rain alert
            if rainfall > self.alert_thresholds["heavy_rain"]["rainfall"]:
                alerts.append({
                    "type": "heavy_rain",
                    "severity": "high",
                    "message_ar": f"🌧️ تحذير: أمطار غزيرة متوقعة في {date[:10]}. تأكد من الصرف!",
                    "message_en": f"🌧️ Warning: Heavy rain expected on {date[:10]}. Ensure drainage!",
                    "date": date,
                    "icon": "🌧️"
                })
            
            # Wind storm alert
            if wind_speed > self.alert_thresholds["wind_storm"]["wind_speed"]:
                alerts.append({
                    "type": "wind_storm",
                    "severity": "high",
                    "message_ar": f"💨 تحذير: رياح قوية في {date[:10]}. ثبت النباتات!",
                    "message_en": f"💨 Warning: Strong winds on {date[:10]}. Secure plants!",
                    "date": date,
                    "icon": "💨"
                })
        
        return alerts
    
    def get_irrigation_recommendation(self, weather_data: Dict, current_soil_moisture: float = 50) -> Dict:
        """
        Get irrigation recommendation based on weather
        
        Args:
            weather_data: Weather prediction data
            current_soil_moisture: Current soil moisture percentage
        
        Returns:
            Irrigation recommendation
        """
        next_3_days = weather_data.get("predictions", [])[:3]
        avg_temp = sum(p.get("temperature", 20) for p in next_3_days) / len(next_3_days) if next_3_days else 20
        total_rainfall = sum(p.get("rainfall", 0) for p in next_3_days)
        
        # Calculate irrigation need
        if total_rainfall > 20:
            recommendation = "no_irrigation"
            message_ar = "🌧️ لا حاجة للري - أمطار كافية متوقعة"
            message_en = "🌧️ No irrigation needed - sufficient rain expected"
        elif avg_temp > 30 and current_soil_moisture < 40:
            recommendation = "increase_irrigation"
            message_ar = "💧 زد الري - حرارة عالية ورطوبة منخفضة"
            message_en = "💧 Increase irrigation - high temperature and low moisture"
        elif current_soil_moisture < 30:
            recommendation = "irrigate_now"
            message_ar = "🚨 ري فوري - رطوبة التربة منخفضة جداً"
            message_en = "🚨 Immediate irrigation - soil moisture very low"
        else:
            recommendation = "normal_irrigation"
            message_ar = "✅ ري عادي - الوضع طبيعي"
            message_en = "✅ Normal irrigation - situation is normal"
        
        return {
            "recommendation": recommendation,
            "message_ar": message_ar,
            "message_en": message_en,
            "current_moisture": current_soil_moisture,
            "expected_rainfall": round(total_rainfall, 1),
            "avg_temperature": round(avg_temp, 1)
        }


# Global service instance
weather_prediction_service = WeatherPredictionService()


