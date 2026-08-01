import datetime
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from models import TimelineEvent, Conversation, Message, HealthProfile

def create_event(
    db: Session,
    user_id: int,
    event_type: str,
    title: str,
    summary: str,
    details: Optional[Dict[str, Any]] = None,
    timestamp: Optional[datetime.datetime] = None
) -> TimelineEvent:
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()

    event = TimelineEvent(
        user_id=user_id,
        event_type=event_type,
        title=title,
        summary=summary,
        details=details or {},
        timestamp=timestamp
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_merged_timeline(db: Session, user_id: int, filter_type: str = "all") -> List[Dict[str, Any]]:
    timeline: List[Dict[str, Any]] = []

    # 1. Custom Timeline Events Table
    query = db.query(TimelineEvent).filter(TimelineEvent.user_id == user_id)
    if filter_type != "all":
        query = query.filter(TimelineEvent.event_type == filter_type)
    
    custom_events = query.all()
    for e in custom_events:
        timeline.append({
            "id": f"event_{e.id}",
            "type": e.event_type,
            "title": e.title,
            "summary": e.summary,
            "details": e.details or {},
            "timestamp": e.timestamp.isoformat() if e.timestamp else datetime.datetime.utcnow().isoformat()
        })

    # 2. Dynamic Conversations (Consultations)
    if filter_type in ["all", "consultation"]:
        conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
        for conv in conversations:
            # find last assistant message for details
            asst_msg = db.query(Message).filter(
                Message.conversation_id == conv.id,
                Message.role == "assistant"
            ).order_by(Message.timestamp.desc()).first()

            analysis = asst_msg.analysis if (asst_msg and asst_msg.analysis) else {}
            doctor = analysis.get("assigned_doctor", "Dr. Elena Rostova (Internal Medicine)")
            ward = analysis.get("ward", "general")
            confidence = analysis.get("confidence", 0.88)
            possible_causes = analysis.get("possible_causes", [])

            summary_text = f"Consultation completed. Primary diagnosis/ward: {ward.upper()} ward."
            if possible_causes:
                summary_text += f" Possible causes: {', '.join(possible_causes[:2])}."

            timeline.append({
                "id": f"conv_{conv.id}",
                "type": "consultation",
                "title": conv.title or "AI Health Consultation",
                "summary": summary_text,
                "doctor": doctor,
                "ward": ward,
                "confidence": confidence,
                "details": {
                    "conversation_id": conv.id,
                    "possible_causes": possible_causes,
                    "recommended_actions": analysis.get("recommended_actions", []),
                    "warning_signs": analysis.get("warning_signs", []),
                    "personalized_advice": analysis.get("personalized_advice", "")
                },
                "timestamp": conv.created_at.isoformat() if conv.created_at else datetime.datetime.utcnow().isoformat()
            })

    # 3. Dynamic Health Profile & Onboarding Events
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    if profile:
        # Profile creation / update event
        if filter_type in ["all", "profile"]:
            timeline.append({
                "id": f"profile_{profile.id}",
                "type": "profile",
                "title": "Health Profile Initialized & Updated",
                "summary": f"Configured profile with age {profile.age or 30}, height {profile.height_cm or 170}cm, weight {profile.weight_kg or 70}kg.",
                "details": {
                    "conditions": profile.conditions or [],
                    "allergies": profile.allergies or [],
                    "medications": profile.medications or [],
                    "goals": profile.goals or []
                },
                "timestamp": profile.updated_at.isoformat() if profile.updated_at else datetime.datetime.utcnow().isoformat()
            })

        # Medication events
        if filter_type in ["all", "medication"] and profile.medications:
            timeline.append({
                "id": f"med_{profile.id}",
                "type": "medication",
                "title": f"Medication Schedule Active ({len(profile.medications)} Rx)",
                "summary": f"Active medications: {', '.join(profile.medications)}.",
                "details": {
                    "medications": profile.medications,
                    "reminders_enabled": True
                },
                "timestamp": profile.updated_at.isoformat() if profile.updated_at else datetime.datetime.utcnow().isoformat()
            })

        # Wellness event
        if filter_type in ["all", "wellness"]:
            timeline.append({
                "id": f"well_{profile.id}",
                "type": "wellness",
                "title": "Wellness Score & Stress Check-in",
                "summary": f"Current mood reported as '{profile.mood or 'Calm'}' with stress score {profile.stress_level or 3}/5.",
                "details": {
                    "sleep_hours": profile.sleep_hours or 7.5,
                    "water_intake": profile.water_intake or 2.5,
                    "stress_level": profile.stress_level or 3,
                    "mood": profile.mood or "Calm"
                },
                "timestamp": profile.updated_at.isoformat() if profile.updated_at else datetime.datetime.utcnow().isoformat()
            })

    # Sort all events reverse chronologically (newest first)
    timeline.sort(key=lambda x: x["timestamp"], reverse=True)
    return timeline


def get_timeline_stats(db: Session, user_id: int) -> Dict[str, Any]:
    # Total consultations count
    total_consultations = db.query(Conversation).filter(Conversation.user_id == user_id).count()

    # Reports count (from MedicalDocument OR TimelineEvent)
    from models import MedicalDocument
    reports_docs_count = db.query(MedicalDocument).filter(MedicalDocument.user_id == user_id).count()
    reports_events_count = db.query(TimelineEvent).filter(
        TimelineEvent.user_id == user_id,
        TimelineEvent.event_type.in_(["report", "report_upload"])
    ).count()
    reports_count = max(reports_docs_count, reports_events_count)

    # Active medications
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    active_medications = len(profile.medications) if (profile and profile.medications) else 0

    # Health score
    health_score = 85
    if profile:
        if profile.sleep_hours and (profile.sleep_hours < 6 or profile.sleep_hours > 9):
            health_score -= 5
        if profile.stress_level and profile.stress_level >= 4:
            health_score -= 8
        if profile.conditions:
            health_score -= (len(profile.conditions) * 3)

    # Last consultation date
    last_conv = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).first()
    last_date = last_conv.created_at.isoformat() if last_conv else None

    return {
        "total_consultations": total_consultations,
        "reports_uploaded": reports_count,
        "active_medications": active_medications,
        "health_score": max(40, min(98, health_score)),
        "last_consultation_date": last_date
    }
