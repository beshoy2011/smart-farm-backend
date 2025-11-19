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
from app.routers import auth, analysis, dashboard, reports, weather

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
        "http://localhost:3000",  # Frontend port
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

