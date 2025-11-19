"""
Dashboard routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app import models, schemas, auth

router = APIRouter()


@router.get("/stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    
    # Total analyses
    total_analyses = db.query(models.Analysis)\
        .filter(models.Analysis.user_id == current_user.id)\
        .count()
    
    # Average plant health
    avg_health = db.query(func.avg(models.Analysis.plant_health_score))\
        .filter(models.Analysis.user_id == current_user.id)\
        .scalar() or 0.0
    
    # Calculate water saved (estimate)
    # Assuming optimal water usage vs actual
    recent_analyses = db.query(models.Analysis)\
        .filter(models.Analysis.user_id == current_user.id)\
        .order_by(models.Analysis.created_at.desc())\
        .limit(10)\
        .all()
    
    total_water_saved = 0.0
    if recent_analyses:
        optimal_water = 2.5  # Optimal liters per day
        for analysis in recent_analyses:
            if analysis.water_needs:
                saved = max(0, (analysis.water_needs - optimal_water) * 7)  # Weekly
                total_water_saved += saved
    
    # Weekly improvement (compare last week vs previous week)
    now = datetime.utcnow()
    last_week = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
    
    last_week_health = db.query(func.avg(models.Analysis.plant_health_score))\
        .filter(
            models.Analysis.user_id == current_user.id,
            models.Analysis.created_at >= last_week
        )\
        .scalar() or 0.0
    
    prev_week_health = db.query(func.avg(models.Analysis.plant_health_score))\
        .filter(
            models.Analysis.user_id == current_user.id,
            models.Analysis.created_at >= two_weeks_ago,
            models.Analysis.created_at < last_week
        )\
        .scalar() or 0.0
    
    weekly_improvement = 0.0
    if prev_week_health > 0:
        weekly_improvement = ((last_week_health - prev_week_health) / prev_week_health) * 100
    
    return {
        "total_analyses": total_analyses,
        "avg_plant_health": float(avg_health),
        "total_water_saved": round(total_water_saved, 2),
        "weekly_improvement": round(weekly_improvement, 2)
    }


@router.get("/progress", response_model=list[schemas.ProgressData])
async def get_progress_data(
    weeks: int = 8,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress tracking data"""
    
    progress_records = db.query(models.ProgressTracking)\
        .filter(models.ProgressTracking.user_id == current_user.id)\
        .order_by(models.ProgressTracking.week_number.desc())\
        .limit(weeks)\
        .all()
    
    # If no records exist, generate from analyses
    if not progress_records:
        # Group analyses by week
        analyses = db.query(models.Analysis)\
            .filter(models.Analysis.user_id == current_user.id)\
            .order_by(models.Analysis.created_at.desc())\
            .limit(weeks * 7)\
            .all()
        
        # Create weekly aggregates
        weekly_data = {}
        for analysis in analyses:
            week_num = (datetime.utcnow() - analysis.created_at).days // 7
            if week_num not in weekly_data:
                weekly_data[week_num] = {
                    "water": [],
                    "fertilizer": [],
                    "health": []
                }
            if analysis.water_needs:
                weekly_data[week_num]["water"].append(analysis.water_needs)
            if analysis.plant_health_score:
                weekly_data[week_num]["health"].append(analysis.plant_health_score)
        
        # Create progress records
        for week_num, data in weekly_data.items():
            progress = models.ProgressTracking(
                user_id=current_user.id,
                week_number=week_num,
                water_usage=sum(data["water"]) / len(data["water"]) if data["water"] else 0.0,
                fertilizer_usage=2.0,  # Default
                plant_health_avg=sum(data["health"]) / len(data["health"]) if data["health"] else 0.0
            )
            db.add(progress)
        
        db.commit()
        progress_records = db.query(models.ProgressTracking)\
            .filter(models.ProgressTracking.user_id == current_user.id)\
            .order_by(models.ProgressTracking.week_number.desc())\
            .limit(weeks)\
            .all()
    
    return progress_records


@router.get("/charts/water-usage")
async def get_water_usage_chart(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get water usage chart data"""
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    analyses = db.query(models.Analysis)\
        .filter(
            models.Analysis.user_id == current_user.id,
            models.Analysis.created_at >= cutoff_date,
            models.Analysis.water_needs.isnot(None)
        )\
        .order_by(models.Analysis.created_at)\
        .all()
    
    chart_data = {
        "labels": [],
        "values": []
    }
    
    for analysis in analyses:
        chart_data["labels"].append(analysis.created_at.strftime("%Y-%m-%d"))
        chart_data["values"].append(analysis.water_needs)
    
    return chart_data


@router.get("/charts/soil-health")
async def get_soil_health_chart(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get soil health timeline chart"""
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    analyses = db.query(models.Analysis)\
        .filter(
            models.Analysis.user_id == current_user.id,
            models.Analysis.created_at >= cutoff_date,
            models.Analysis.soil_quality.isnot(None)
        )\
        .order_by(models.Analysis.created_at)\
        .all()
    
    # Map soil types to scores
    soil_scores = {
        "loamy": 0.9,
        "silty": 0.7,
        "clay": 0.6,
        "sandy": 0.5
    }
    
    chart_data = {
        "labels": [],
        "values": []
    }
    
    for analysis in analyses:
        chart_data["labels"].append(analysis.created_at.strftime("%Y-%m-%d"))
        score = soil_scores.get(analysis.soil_quality.lower(), 0.5)
        chart_data["values"].append(score)
    
    return chart_data

