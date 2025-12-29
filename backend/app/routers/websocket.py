"""
WebSocket routes for real-time monitoring
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app import models, auth
from typing import Dict, List
import asyncio
import json
from datetime import datetime

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a user's WebSocket"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a user's WebSocket"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to specific user"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for conn in disconnected:
                self.disconnect(conn, user_id)
    
    async def broadcast_to_user(self, user_id: int, message: dict):
        """Broadcast message to all connections of a user"""
        await self.send_personal_message(message, user_id)


manager = ConnectionManager()


async def get_latest_plant_data(user_id: int, db: Session) -> dict:
    """Get latest plant analysis data for user"""
    latest_analysis = db.query(models.Analysis).filter(
        models.Analysis.user_id == user_id
    ).order_by(models.Analysis.created_at.desc()).first()
    
    if not latest_analysis:
        return {
            "type": "no_data",
            "message": "لا توجد بيانات بعد"
        }
    
    # Get all analyses for stats
    all_analyses = db.query(models.Analysis).filter(
        models.Analysis.user_id == user_id
    ).all()
    
    total_analyses = len(all_analyses)
    avg_health = sum(a.plant_health_score or 0 for a in all_analyses) / total_analyses if all_analyses else 0
    total_water_saved = sum(a.cost_savings or 0 for a in all_analyses)
    
    return {
        "type": "plant_update",
        "timestamp": datetime.now().isoformat(),
        "health_score": latest_analysis.plant_health_score or 0,
        "water_level": latest_analysis.water_level_percent or 0,
        "soil_moisture": latest_analysis.soil_moisture_percent or 0,
        "disease_probability": latest_analysis.disease_probability or 0,
        "alerts": {
            "water": latest_analysis.water_alert or False,
            "disease": latest_analysis.disease_alert or False,
            "temperature": latest_analysis.temperature_alert or False,
            "fertilizer": latest_analysis.fertilizer_alert or False,
        },
        "warnings": latest_analysis.warnings or {},
        "stats": {
            "total_analyses": total_analyses,
            "avg_health": round(avg_health, 1),
            "total_water_saved": round(total_water_saved, 2),
        },
        "latest_analysis_id": latest_analysis.id
    }


@router.websocket("/ws/monitoring/{user_id}")
async def websocket_monitoring(
    websocket: WebSocket, 
    user_id: int,
    token: str = None
):
    """
    WebSocket endpoint for real-time plant monitoring
    Note: In production, you should verify the token here
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Send initial data
        db = SessionLocal()
        try:
            initial_data = await get_latest_plant_data(user_id, db)
            await websocket.send_json(initial_data)
        finally:
            db.close()
        
        # Keep connection alive and send updates
        while True:
            # Wait for client ping or send update every 5 seconds
            try:
                # Try to receive message (ping) with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=5.0)
                # If we receive data, echo it back or handle it
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # Timeout - send update
                db = SessionLocal()
                try:
                    update_data = await get_latest_plant_data(user_id, db)
                    await websocket.send_json(update_data)
                finally:
                    db.close()
            except:
                break
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)


@router.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(
    websocket: WebSocket,
    user_id: int
):
    """WebSocket for real-time notifications"""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # This will be used to push notifications
            await asyncio.sleep(1)
            # In production, this would listen to a queue/event system
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


async def broadcast_achievement(user_id: int, achievement: dict):
    """Broadcast achievement unlock to user's WebSocket connections"""
    message = {
        "type": "achievement_unlocked",
        "achievement": achievement,
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_user(user_id, message)


async def broadcast_alert(user_id: int, alert_type: str, message: str):
    """Broadcast alert to user's WebSocket connections"""
    alert_data = {
        "type": "alert",
        "alert_type": alert_type,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_to_user(user_id, alert_data)


