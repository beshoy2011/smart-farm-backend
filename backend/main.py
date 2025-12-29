"""
SmartFarm AI - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.database import engine, Base
from app.routers import auth, analysis, dashboard, reports, weather, websocket, achievements, notifications, chatbot, plant_comparison, weekly_recommendations, timelapse, smart_irrigation, analytics, daily_recommendations, tasks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartFarm AI API",
    description="AI-powered agricultural analysis platform",
    version="1.0.0"
)

# CORS middleware
# Allow all origins in development, restrict in production
is_production = os.getenv("ENVIRONMENT") == "production"

if is_production:
    # In production, use specific origins from environment variable
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
    if not allowed_origins:
        allowed_origins = ["http://localhost:80"]  # Default production origin
else:
    # In development, allow common localhost ports
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://localhost:80",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:80",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Mount static files
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(websocket.router, tags=["WebSocket"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["Achievements"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(plant_comparison.router, prefix="/api/plant-comparison", tags=["Plant Comparison"])
app.include_router(weekly_recommendations.router, prefix="/api/weekly-recommendations", tags=["Weekly Recommendations"])
app.include_router(timelapse.router, prefix="/api/timelapse", tags=["Time-lapse"])
app.include_router(smart_irrigation.router, prefix="/api/irrigation", tags=["Smart Irrigation"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Advanced Analytics"])
app.include_router(daily_recommendations.router, prefix="/api/daily-recommendations", tags=["Daily Recommendations"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Task Management"])


@app.get("/")
async def root():
    return {
        "message": "SmartFarm AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

