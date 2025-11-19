"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class GoogleAuthRequest(BaseModel):
    access_token: str


# Analysis schemas
class AnalysisBase(BaseModel):
    plant_type: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    image_path: str
    plant_health_score: Optional[float] = None
    water_needs: Optional[float] = None
    soil_quality: Optional[str] = None
    fertilizer_deficiency: Optional[Dict[str, Any]] = None
    diseases: Optional[List[Dict[str, Any]]] = None
    pests: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[Dict[str, Any]] = None
    plant_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PlantAIResponse(BaseModel):
    analysis_id: int
    user_id: int
    image_path: str
    plant_type: Optional[str] = None
    plant_health_score: Optional[float] = None
    water_needs: Optional[float] = None
    water_level_percent: Optional[float] = None
    soil_quality: Optional[str] = None
    soil_moisture_percent: Optional[float] = None
    fertilizer_deficiency: Optional[Dict[str, Any]] = None
    detected_diseases: Optional[List[Dict[str, Any]]] = None
    diseases: Optional[List[Dict[str, Any]]] = None
    pests: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    nutrient_profile: Optional[Dict[str, Any]] = None
    fertilizer_need_percent: Optional[float] = None
    leaf_color_index: Optional[float] = None
    dryness_factor: Optional[float] = None
    nitrogen_deficiency_probability: Optional[float] = None
    growth_stage: Optional[Dict[str, Any]] = None
    explainability: Optional[Dict[str, Any]] = None
    analysis_metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    created_at: datetime
    # Advanced features
    disease_probability: Optional[float] = None
    predicted_diseases: Optional[List[Dict[str, Any]]] = None
    soil_ph: Optional[float] = None
    soil_nitrogen: Optional[float] = None
    soil_phosphorus: Optional[float] = None
    soil_potassium: Optional[float] = None
    nitrogen_level: Optional[float] = None
    phosphorus_level: Optional[float] = None
    potassium_level: Optional[float] = None
    recommended_fertilizer_amount: Optional[float] = None
    fertilizer_type: Optional[str] = None
    irrigation_needed: Optional[bool] = None
    irrigation_duration_minutes: Optional[float] = None
    warnings: Optional[Dict[str, Any]] = None
    temperature_alert: Optional[bool] = None
    water_alert: Optional[bool] = None
    fertilizer_alert: Optional[bool] = None
    disease_alert: Optional[bool] = None
    estimated_water_cost: Optional[float] = None
    estimated_fertilizer_cost: Optional[float] = None
    cost_savings: Optional[float] = None
    efficiency_percentage: Optional[float] = None
    ai_summary_arabic: Optional[str] = None
    ai_summary_english: Optional[str] = None
    leaf_damage_percent: Optional[float] = None


# Weather schemas
class WeatherResponse(BaseModel):
    location: str
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: Optional[float] = None
    recorded_at: datetime

    class Config:
        from_attributes = True


# Dashboard schemas
class DashboardStats(BaseModel):
    total_analyses: int
    avg_plant_health: float
    total_water_saved: float
    weekly_improvement: float


class ProgressData(BaseModel):
    week_number: int
    water_usage: float
    fertilizer_usage: float
    plant_health_avg: float
    created_at: datetime

    class Config:
        from_attributes = True


# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class PlantComparisonRequest(BaseModel):
    analysis_id_1: int
    analysis_id_2: int

