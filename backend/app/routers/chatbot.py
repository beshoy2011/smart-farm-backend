"""
Chatbot routes for AI agricultural assistance
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app import models, auth
from app.services.enhanced_chatbot_service import enhanced_chatbot as chatbot
from typing import List, Optional

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    language: Optional[str] = "ar"


class ChatResponse(BaseModel):
    response: str
    topic: str
    confidence: float
    timestamp: str


class ConversationHistory(BaseModel):
    user_message: str
    bot_response: str
    timestamp: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_message: ChatMessage,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI agricultural assistant"""
    try:
        result = chatbot.get_response(
            user_id=current_user.id,
            message=chat_message.message,
            language=chat_message.language or "ar",
            db=db
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


@router.get("/history", response_model=List[ConversationHistory])
async def get_history(
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation history"""
    try:
        history = chatbot.get_conversation_history(current_user.id, limit)
        return [ConversationHistory(**msg) for msg in history]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting history: {str(e)}"
        )


@router.delete("/history")
async def clear_history(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Clear conversation history"""
    try:
        chatbot.clear_history(current_user.id)
        return {"message": "History cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing history: {str(e)}"
        )


