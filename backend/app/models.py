"""
Database models for SmartFarm AI
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    google_id = Column(String, unique=True, index=True, nullable=True)
    profile_picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analyses = relationship("Analysis", back_populates="owner")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String, nullable=False)
    
    # Analysis results
    plant_health_score = Column(Float, nullable=True)
    water_needs = Column(Float, nullable=True)
    water_level_percent = Column(Float, nullable=True)
    soil_quality = Column(String, nullable=True)
    soil_moisture_percent = Column(Float, nullable=True)
    fertilizer_deficiency = Column(JSON, nullable=True)
    diseases = Column(JSON, nullable=True)
    pests = Column(JSON, nullable=True)
    
    # Advanced soil analysis
    soil_ph = Column(Float, nullable=True)
    soil_nitrogen = Column(Float, nullable=True)
    soil_phosphorus = Column(Float, nullable=True)
    soil_potassium = Column(Float, nullable=True)
    
    # Disease prediction
    disease_probability = Column(Float, nullable=True)
    predicted_diseases = Column(JSON, nullable=True)
    
    # Nutrient analysis (NPK)
    nutrient_profile = Column(JSON, nullable=True)
    nitrogen_level = Column(Float, nullable=True)
    phosphorus_level = Column(Float, nullable=True)
    potassium_level = Column(Float, nullable=True)
    
    # Fertilizer optimization
    fertilizer_need_percent = Column(Float, nullable=True)
    recommended_fertilizer_amount = Column(Float, nullable=True)
    fertilizer_type = Column(String, nullable=True)
    
    # Plant condition details
    leaf_damage_percent = Column(Float, nullable=True)
    growth_stage = Column(JSON, nullable=True)
    dryness_factor = Column(Float, nullable=True)
    leaf_color_index = Column(Float, nullable=True)
    
    # AI analysis metadata
    ai_summary_arabic = Column(Text, nullable=True)
    ai_summary_english = Column(Text, nullable=True)
    explainability = Column(JSON, nullable=True)
    analysis_metadata = Column(JSON, nullable=True)
    
    # Recommendations
    recommendations = Column(JSON, nullable=True)
    weekly_recommendations = Column(JSON, nullable=True)
    
    # Warnings and alerts
    warnings = Column(JSON, nullable=True)
    temperature_alert = Column(Boolean, default=False)
    water_alert = Column(Boolean, default=False)
    fertilizer_alert = Column(Boolean, default=False)
    disease_alert = Column(Boolean, default=False)
    
    # Automatic irrigation
    irrigation_needed = Column(Boolean, default=False)
    irrigation_duration_minutes = Column(Float, nullable=True)
    
    # Cost optimization
    estimated_water_cost = Column(Float, nullable=True)
    estimated_fertilizer_cost = Column(Float, nullable=True)
    cost_savings = Column(Float, nullable=True)
    efficiency_percentage = Column(Float, nullable=True)
    
    # Metadata
    plant_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="analyses")


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())


class ProgressTracking(Base):
    __tablename__ = "progress_tracking"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week_number = Column(Integer, nullable=False)
    water_usage = Column(Float, nullable=False)
    fertilizer_usage = Column(Float, nullable=False)
    plant_health_avg = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlantComparison(Base):
    __tablename__ = "plant_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_id_1 = Column(Integer, ForeignKey("analyses.id"))
    analysis_id_2 = Column(Integer, ForeignKey("analyses.id"))
    comparison_results = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AIAccuracyTracking(Base):
    __tablename__ = "ai_accuracy_tracking"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    prediction_type = Column(String, nullable=False)  # disease, water, fertilizer, etc.
    predicted_value = Column(Float, nullable=True)
    actual_value = Column(Float, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WeeklyRecommendation(Base):
    __tablename__ = "weekly_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week_start_date = Column(DateTime(timezone=True), nullable=False)
    recommendations = Column(JSON, nullable=True)
    plant_ids = Column(JSON, nullable=True)  # List of analysis IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())

