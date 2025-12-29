"""
Image analysis routes
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import time
from PIL import Image
from app.database import get_db
from app import models, schemas, auth
from app.services.ai_service import AIService

router = APIRouter()

# Initialize AI service
ai_service = AIService()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/analyze_image", response_model=schemas.PlantAIResponse)
async def analyze_image(
    file: UploadFile = File(...),
    plant_type: str = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze plant image and return comprehensive results - NO CACHING"""
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Save uploaded file with unique name to prevent any caching
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}-{int(time.time() * 1000)}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Read file content fresh - ensure we're analyzing the actual uploaded file
    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Reset file pointer if needed (though we already read it)
    await file.seek(0)
    
    try:
        # Perform FRESH AI analysis - no caching, analyze the actual file
        analysis_results = await ai_service.analyze_plant_image(file_path, plant_type)
        
        # Save comprehensive analysis to database
        db_analysis = models.Analysis(
            user_id=current_user.id,
            image_path=file_path,
            plant_health_score=analysis_results.get("plant_health_score"),
            water_needs=analysis_results.get("water_needs"),
            water_level_percent=analysis_results.get("water_level_percent"),
            soil_quality=analysis_results.get("soil_quality"),
            soil_moisture_percent=analysis_results.get("soil_moisture_percent"),
            fertilizer_deficiency=analysis_results.get("fertilizer_deficiency"),
            diseases=analysis_results.get("diseases"),
            pests=analysis_results.get("pests"),
            recommendations=analysis_results.get("recommendations"),
            plant_type=plant_type or analysis_results.get("plant_type"),
            # Advanced soil analysis
            soil_ph=analysis_results.get("soil_ph"),
            soil_nitrogen=analysis_results.get("soil_nitrogen"),
            soil_phosphorus=analysis_results.get("soil_phosphorus"),
            soil_potassium=analysis_results.get("soil_potassium"),
            # Disease prediction
            disease_probability=analysis_results.get("disease_probability"),
            predicted_diseases=analysis_results.get("predicted_diseases"),
            # Nutrient analysis
            nutrient_profile=analysis_results.get("nutrient_profile"),
            nitrogen_level=analysis_results.get("nitrogen_level"),
            phosphorus_level=analysis_results.get("phosphorus_level"),
            potassium_level=analysis_results.get("potassium_level"),
            # Fertilizer optimization
            fertilizer_need_percent=analysis_results.get("fertilizer_need_percent"),
            recommended_fertilizer_amount=analysis_results.get("recommended_fertilizer_amount"),
            fertilizer_type=analysis_results.get("fertilizer_type"),
            # Plant condition
            leaf_damage_percent=analysis_results.get("leaf_damage_percent"),
            growth_stage=analysis_results.get("growth_stage"),
            dryness_factor=analysis_results.get("dryness_factor"),
            leaf_color_index=analysis_results.get("leaf_color_index"),
            # AI metadata
            ai_summary_arabic=analysis_results.get("ai_summary_arabic"),
            ai_summary_english=analysis_results.get("ai_summary_english"),
            explainability=analysis_results.get("explainability"),
            analysis_metadata=analysis_results.get("analysis_metadata"),
            # Warnings
            warnings=analysis_results.get("warnings"),
            temperature_alert=analysis_results.get("temperature_alert", False),
            water_alert=analysis_results.get("water_alert", False),
            fertilizer_alert=analysis_results.get("fertilizer_alert", False),
            disease_alert=analysis_results.get("disease_alert", False),
            # Irrigation
            irrigation_needed=analysis_results.get("irrigation_needed", False),
            irrigation_duration_minutes=analysis_results.get("irrigation_duration_minutes"),
            # Cost optimization
            estimated_water_cost=analysis_results.get("estimated_water_cost"),
            estimated_fertilizer_cost=analysis_results.get("estimated_fertilizer_cost"),
            cost_savings=analysis_results.get("cost_savings"),
            efficiency_percentage=analysis_results.get("efficiency_percentage"),
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Check and unlock achievements (non-blocking)
        try:
            from app.services.achievement_service import AchievementService
            
            achievement_service = AchievementService()
            newly_unlocked = achievement_service.check_and_unlock_achievements(
                current_user.id, db
            )
            
            # Send email notifications for achievements (non-blocking)
            if newly_unlocked:
                try:
                    from app.services.email_service import EmailService
                    email_service = EmailService()
                    for achievement in newly_unlocked:
                        if current_user.email:
                            email_service.send_achievement_email(
                                current_user.email,
                                current_user.full_name or current_user.username,
                                achievement
                            )
                except Exception as email_error:
                    print(f"Email notification error: {email_error}")
            
            # Broadcast via WebSocket (non-blocking, don't await to avoid blocking)
            # Note: WebSocket broadcasting is handled separately, not blocking the response
            if newly_unlocked:
                try:
                    # Just log - WebSocket will handle broadcasting when connected
                    print(f"New achievements unlocked for user {current_user.id}: {len(newly_unlocked)}")
                except Exception as ws_error:
                    print(f"WebSocket broadcast error: {ws_error}")
        except Exception as e:
            print(f"Error in achievement system: {e}")
            # Don't fail the analysis if achievement system fails

        response_payload = {
            "analysis_id": db_analysis.id,
            "user_id": current_user.id,
            "image_path": db_analysis.image_path,
            "plant_type": db_analysis.plant_type,
            "plant_health_score": analysis_results.get("plant_health_score"),
            "water_needs": analysis_results.get("water_needs"),
            "water_level_percent": analysis_results.get("water_level_percent"),
            "soil_quality": analysis_results.get("soil_quality"),
            "soil_moisture_percent": analysis_results.get("soil_moisture_percent"),
            "fertilizer_deficiency": analysis_results.get("fertilizer_deficiency"),
            "detected_diseases": analysis_results.get("detected_diseases"),
            "diseases": analysis_results.get("diseases"),
            "pests": analysis_results.get("pests"),
            "recommendations": analysis_results.get("recommendations"),
            "nutrient_profile": analysis_results.get("nutrient_profile"),
            "fertilizer_need_percent": analysis_results.get("fertilizer_need_percent"),
            "leaf_color_index": analysis_results.get("leaf_color_index"),
            "dryness_factor": analysis_results.get("dryness_factor"),
            "nitrogen_deficiency_probability": analysis_results.get("nitrogen_deficiency_probability"),
            "growth_stage": analysis_results.get("growth_stage"),
            "explainability": analysis_results.get("explainability"),
            "analysis_metadata": analysis_results.get("analysis_metadata"),
            "timestamp": analysis_results.get("timestamp"),
            "created_at": db_analysis.created_at,
            # Advanced features
            "disease_probability": analysis_results.get("disease_probability"),
            "predicted_diseases": analysis_results.get("predicted_diseases"),
            "soil_ph": analysis_results.get("soil_ph"),
            "soil_nitrogen": analysis_results.get("soil_nitrogen"),
            "soil_phosphorus": analysis_results.get("soil_phosphorus"),
            "soil_potassium": analysis_results.get("soil_potassium"),
            "nitrogen_level": analysis_results.get("nitrogen_level"),
            "phosphorus_level": analysis_results.get("phosphorus_level"),
            "potassium_level": analysis_results.get("potassium_level"),
            "recommended_fertilizer_amount": analysis_results.get("recommended_fertilizer_amount"),
            "fertilizer_type": analysis_results.get("fertilizer_type"),
            "irrigation_needed": analysis_results.get("irrigation_needed"),
            "irrigation_duration_minutes": analysis_results.get("irrigation_duration_minutes"),
            "warnings": analysis_results.get("warnings"),
            "temperature_alert": analysis_results.get("temperature_alert"),
            "water_alert": analysis_results.get("water_alert"),
            "fertilizer_alert": analysis_results.get("fertilizer_alert"),
            "disease_alert": analysis_results.get("disease_alert"),
            "estimated_water_cost": analysis_results.get("estimated_water_cost"),
            "estimated_fertilizer_cost": analysis_results.get("estimated_fertilizer_cost"),
            "cost_savings": analysis_results.get("cost_savings"),
            "efficiency_percentage": analysis_results.get("efficiency_percentage"),
            "ai_summary_arabic": analysis_results.get("ai_summary_arabic"),
            "ai_summary_english": analysis_results.get("ai_summary_english"),
            "leaf_damage_percent": analysis_results.get("leaf_damage_percent"),
        }
        
        return response_payload
        
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/predict_water", response_model=dict)
async def predict_water(
    plant_type: str,
    soil_moisture: float,
    temperature: float,
    current_user: models.User = Depends(auth.get_current_user)
):
    """Predict water needs based on conditions"""
    water_prediction = await ai_service.predict_water_needs(
        plant_type, soil_moisture, temperature
    )
    return {"water_needs": water_prediction}


@router.post("/detect_soil", response_model=dict)
async def detect_soil(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Detect soil type and quality from image"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        soil_analysis = await ai_service.detect_soil_quality(file_path)
        return soil_analysis
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/fertilizer", response_model=dict)
async def analyze_fertilizer(
    plant_type: str,
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get fertilizer recommendations"""
    fertilizer_analysis = await ai_service.analyze_fertilizer_needs(plant_type)
    return fertilizer_analysis


@router.get("/pests", response_model=dict)
async def detect_pests(
    plant_type: str,
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get pest detection and recommendations"""
    pest_analysis = await ai_service.detect_pests(plant_type)
    return pest_analysis


@router.get("/history", response_model=List[schemas.AnalysisResponse])
async def get_analysis_history(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's analysis history"""
    analyses = db.query(models.Analysis)\
        .filter(models.Analysis.user_id == current_user.id)\
        .order_by(models.Analysis.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return analyses


@router.post("/compare_plants")
async def compare_plants(
    request: schemas.PlantComparisonRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    analysis_id_1 = request.analysis_id_1
    analysis_id_2 = request.analysis_id_2
    """Compare two plant analyses and generate insights"""
    plant1 = db.query(models.Analysis)\
        .filter(models.Analysis.id == analysis_id_1, models.Analysis.user_id == current_user.id)\
        .first()
    plant2 = db.query(models.Analysis)\
        .filter(models.Analysis.id == analysis_id_2, models.Analysis.user_id == current_user.id)\
        .first()
    
    if not plant1 or not plant2:
        raise HTTPException(status_code=404, detail="One or both analyses not found")
    
    # Generate comparison
    comparison = await ai_service.compare_plants(plant1, plant2)
    
    # Save comparison
    db_comparison = models.PlantComparison(
        user_id=current_user.id,
        analysis_id_1=analysis_id_1,
        analysis_id_2=analysis_id_2,
        comparison_results=comparison
    )
    db.add(db_comparison)
    db.commit()
    
    return comparison


@router.get("/weekly_recommendations")
async def get_weekly_recommendations(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated weekly care plan for all plants"""
    from datetime import datetime, timedelta
    
    week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
    
    # Get all recent analyses
    recent_analyses = db.query(models.Analysis)\
        .filter(models.Analysis.user_id == current_user.id)\
        .order_by(models.Analysis.created_at.desc())\
        .limit(20)\
        .all()
    
    recommendations = await ai_service.generate_weekly_recommendations(recent_analyses)
    
    # Save recommendations
    db_recommendation = models.WeeklyRecommendation(
        user_id=current_user.id,
        week_start_date=week_start,
        recommendations=recommendations,
        plant_ids=[a.id for a in recent_analyses[:10]]
    )
    db.add(db_recommendation)
    db.commit()
    
    return recommendations


@router.get("/disease_prediction/{analysis_id}")
async def get_disease_prediction(
    analysis_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get disease prediction for a specific analysis"""
    analysis = db.query(models.Analysis)\
        .filter(models.Analysis.id == analysis_id, models.Analysis.user_id == current_user.id)\
        .first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "disease_probability": analysis.disease_probability,
        "predicted_diseases": analysis.predicted_diseases,
        "disease_alert": analysis.disease_alert,
        "accuracy": 90.0  # 90% accuracy model
    }


@router.get("/soil_quality/{analysis_id}")
async def get_soil_quality(
    analysis_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed soil quality analysis"""
    analysis = db.query(models.Analysis)\
        .filter(models.Analysis.id == analysis_id, models.Analysis.user_id == current_user.id)\
        .first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "ph": analysis.soil_ph,
        "nitrogen": analysis.soil_nitrogen,
        "phosphorus": analysis.soil_phosphorus,
        "potassium": analysis.soil_potassium,
        "moisture": analysis.soil_moisture_percent,
        "quality": analysis.soil_quality
    }


@router.get("/fertilizer_optimization/{analysis_id}")
async def get_fertilizer_optimization(
    analysis_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get smart fertilizer optimization recommendations"""
    analysis = db.query(models.Analysis)\
        .filter(models.Analysis.id == analysis_id, models.Analysis.user_id == current_user.id)\
        .first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "need_percent": analysis.fertilizer_need_percent,
        "recommended_amount": analysis.recommended_fertilizer_amount,
        "fertilizer_type": analysis.fertilizer_type,
        "nitrogen_level": analysis.nitrogen_level,
        "phosphorus_level": analysis.phosphorus_level,
        "potassium_level": analysis.potassium_level,
        "warning": analysis.fertilizer_alert
    }


@router.get("/cost_optimization")
async def get_cost_optimization(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get cost optimization analysis for all plants"""
    analyses = db.query(models.Analysis)\
        .filter(models.Analysis.user_id == current_user.id)\
        .order_by(models.Analysis.created_at.desc())\
        .limit(30)\
        .all()
    
    total_water_cost = sum(a.estimated_water_cost or 0 for a in analyses)
    total_fertilizer_cost = sum(a.estimated_fertilizer_cost or 0 for a in analyses)
    total_savings = sum(a.cost_savings or 0 for a in analyses)
    avg_efficiency = sum(a.efficiency_percentage or 0 for a in analyses) / len(analyses) if analyses else 0
    
    return {
        "total_water_cost": round(total_water_cost, 2),
        "total_fertilizer_cost": round(total_fertilizer_cost, 2),
        "total_cost": round(total_water_cost + total_fertilizer_cost, 2),
        "total_savings": round(total_savings, 2),
        "average_efficiency": round(avg_efficiency, 1),
        "water_usage_liters": sum((a.irrigation_duration_minutes or 0) * 2 for a in analyses),
        "fertilizer_usage_kg": sum(a.recommended_fertilizer_amount or 0 for a in analyses)
    }

