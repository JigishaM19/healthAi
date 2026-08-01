from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional

from database import get_db
from models import User
from auth import get_current_user
from services.insight_generator import generate_health_insights, answer_memory_question
from services.trend_analysis_service import get_tracked_trends, get_test_history
from services.health_memory_service import get_user_memories

router = APIRouter(tags=["Health Memory & Lab Trends"])

class MemoryQueryRequest(BaseModel):
    question: str

@router.get("/health-insights")
async def get_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns AI-generated health insights, lab alerts, medication adherence %, and summary.
    """
    insights = await generate_health_insights(db, current_user.id)
    return insights

@router.get("/health-trends")
def get_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns all tracked laboratory trends with latest value, previous value, change, percent change, and trend direction.
    """
    trends = get_tracked_trends(db, current_user.id)
    return trends

@router.get("/health-trends/{test_name}")
def get_parameter_history(
    test_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns complete historical timeline of one lab parameter (e.g., Hemoglobin, Glucose, Cholesterol).
    """
    history = get_test_history(db, current_user.id, test_name)
    return history

@router.post("/ask-memory")
async def ask_memory(
    body: MemoryQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Answers AI health memory queries comparing past vs present reports and medications.
    """
    if not body.question or not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    res = await answer_memory_question(db, current_user.id, body.question)
    return res

@router.get("/health-memories")
def list_memories(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns chronological list of stored AI Health Memory entries.
    """
    memories = get_user_memories(db, current_user.id, limit)
    return memories
