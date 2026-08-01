from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from database import get_db
from models import User
from auth import get_current_user
from services.timeline_service import get_merged_timeline, create_event, get_timeline_stats

router = APIRouter(tags=["Health Timeline"])

class TimelineEventCreateInput(BaseModel):
    event_type: str # "consultation", "report", "medication", "wellness", "profile"
    title: str
    summary: str
    details: Optional[Dict[str, Any]] = None

@router.get("/timeline")
def get_timeline(
    type: str = Query("all", description="Filter by event category: all, consultation, report, medication, wellness, profile"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's personal chronological medical history merged from consultations, reports, medications, wellness checks, and profile updates.
    """
    events = get_merged_timeline(db, current_user.id, filter_type=type)
    return events


@router.post("/timeline/event")
def add_timeline_event(
    event_input: TimelineEventCreateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Append a new event to user's medical timeline (e.g. report uploads, custom notes).
    """
    event = create_event(
        db=db,
        user_id=current_user.id,
        event_type=event_input.event_type,
        title=event_input.title,
        summary=event_input.summary,
        details=event_input.details
    )
    return {
        "id": f"event_{event.id}",
        "type": event.event_type,
        "title": event.title,
        "summary": event.summary,
        "details": event.details,
        "timestamp": event.timestamp.isoformat()
    }


@router.get("/timeline/stats")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get high-level metric stats for the Health Timeline header.
    """
    return get_timeline_stats(db, current_user.id)
