"""
Weather data routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import requests
import os
from app.database import get_db
from app import models, schemas, auth

router = APIRouter()

# Weather API key (use environment variable in production)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your-api-key")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


@router.get("/current")
async def get_current_weather(
    location: str = "Cairo,EG",
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get current weather data"""
    
    try:
        # Try to get from database first (last 1 hour)
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(hours=1)
        
        recent_weather = db.query(models.WeatherData)\
            .filter(
                models.WeatherData.location == location,
                models.WeatherData.recorded_at >= cutoff
            )\
            .order_by(models.WeatherData.recorded_at.desc())\
            .first()
        
        if recent_weather:
            return recent_weather
        
        # Fetch from API
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            # Fallback to mock data
            return _get_mock_weather(location, db)
        
        data = response.json()
        
        # Save to database
        weather_data = models.WeatherData(
            location=location,
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            rainfall=data.get("rain", {}).get("1h", 0.0) if "rain" in data else 0.0,
            wind_speed=data.get("wind", {}).get("speed", 0.0)
        )
        db.add(weather_data)
        db.commit()
        db.refresh(weather_data)
        
        return weather_data
        
    except Exception as e:
        # Fallback to mock data
        return _get_mock_weather(location, db)


@router.get("/recommendations")
async def get_weather_recommendations(
    location: str = "Cairo,EG",
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get weather-aware irrigation recommendations"""
    
    weather = await get_current_weather(location, current_user, db)
    
    recommendations = []
    
    # Temperature-based recommendations
    if weather.temperature > 30:
        recommendations.append({
            "type": "water",
            "priority": "high",
            "message": "High temperature detected. Increase irrigation frequency.",
            "action": "Water plants in early morning or evening to reduce evaporation."
        })
    elif weather.temperature < 10:
        recommendations.append({
            "type": "water",
            "priority": "low",
            "message": "Low temperature. Reduce watering to prevent root rot.",
            "action": "Water less frequently during cold weather."
        })
    
    # Rainfall-based recommendations
    if weather.rainfall > 5.0:
        recommendations.append({
            "type": "water",
            "priority": "high",
            "message": "Recent rainfall detected. Skip scheduled irrigation.",
            "action": "Monitor soil moisture before next watering."
        })
    
    # Humidity-based recommendations
    if weather.humidity > 80:
        recommendations.append({
            "type": "disease",
            "priority": "medium",
            "message": "High humidity increases disease risk.",
            "action": "Ensure good air circulation and monitor for fungal diseases."
        })
    elif weather.humidity < 30:
        recommendations.append({
            "type": "water",
            "priority": "medium",
            "message": "Low humidity increases water loss.",
            "action": "Consider mulching to retain soil moisture."
        })
    
    return {
        "weather": weather,
        "recommendations": recommendations
    }


def _get_mock_weather(location: str, db: Session) -> models.WeatherData:
    """Generate mock weather data"""
    import random
    
    weather_data = models.WeatherData(
        location=location,
        temperature=random.uniform(20, 30),
        humidity=random.uniform(40, 70),
        rainfall=random.uniform(0, 2),
        wind_speed=random.uniform(5, 15)
    )
    db.add(weather_data)
    db.commit()
    db.refresh(weather_data)
    return weather_data

