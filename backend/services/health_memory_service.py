import datetime
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from models import HealthMemory, LabMeasurement, Medication, MedicalDocument, HealthProfile

def create_memory_entry(
    db: Session,
    user_id: int,
    memory_type: str,
    title: str,
    summary: str,
    source_type: Optional[str] = None,
    source_id: Optional[int] = None,
    metadata_json: Optional[Dict[str, Any]] = None
) -> HealthMemory:
    """
    Creates and persists a new Health Memory entry for a user.
    """
    memory = HealthMemory(
        user_id=user_id,
        memory_type=memory_type,
        title=title,
        summary=summary,
        source_type=source_type,
        source_id=source_id,
        metadata_json=metadata_json or {},
        created_at=datetime.datetime.utcnow()
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory

def get_user_memories(db: Session, user_id: int, limit: int = 15) -> List[Dict[str, Any]]:
    memories = db.query(HealthMemory).filter(
        HealthMemory.user_id == user_id
    ).order_by(HealthMemory.created_at.desc()).limit(limit).all()

    return [{
        "id": m.id,
        "memory_type": m.memory_type,
        "title": m.title,
        "summary": m.summary,
        "metadata": m.metadata_json,
        "created_at": m.created_at.isoformat() if m.created_at else None
    } for m in memories]

def build_memory_prompt_context(db: Session, user_id: int, user_query: str = "") -> str:
    """
    Retrieves historical lab measurements, active medications, and memories,
    formatting them into a concise context block for AI prompt injection.
    """
    context_parts = []

    # 1. Active Medications History
    meds = db.query(Medication).filter(Medication.user_id == user_id).all()
    if meds:
        med_str = ", ".join([f"{m.medicine_name} ({m.dosage or 'standard dose'}, {m.frequency or 'daily'})" for m in meds])
        context_parts.append(f"• ACTIVE MEDICATIONS HISTORY: {med_str}")

    # 2. Lab Measurements Summary
    labs = db.query(LabMeasurement).filter(LabMeasurement.user_id == user_id).order_by(LabMeasurement.test_date.desc()).all()
    if labs:
        # Group by test_name
        test_history: Dict[str, List[str]] = {}
        for lab in labs:
            if lab.test_name not in test_history:
                test_history[lab.test_name] = []
            if len(test_history[lab.test_name]) < 3: # Keep last 3 values per test
                dt = lab.test_date.strftime("%Y-%m-%d") if lab.test_date else "recent"
                test_history[lab.test_name].append(f"{lab.value} {lab.unit or ''} ({dt}, status: {lab.status or 'Normal'})")

        lab_lines = []
        for test, hist in test_history.items():
            lab_lines.append(f"  - {test}: {' -> '.join(reversed(hist))}")
        
        context_parts.append("• HISTORICAL LABORATORY MEASUREMENTS:\n" + "\n".join(lab_lines))

    # 3. Recent Health Memories
    memories = db.query(HealthMemory).filter(HealthMemory.user_id == user_id).order_by(HealthMemory.created_at.desc()).limit(5).all()
    if memories:
        mem_lines = [f"  - [{m.memory_type.upper()}] {m.title}: {m.summary}" for m in memories]
        context_parts.append("• RECENT HEALTH MEMORIES & INSIGHTS:\n" + "\n".join(mem_lines))

    if not context_parts:
        return ""

    return "\n--- HISTORICAL HEALTH MEMORY & LAB TREND CONTEXT ---\n" + "\n\n".join(context_parts) + "\n----------------------------------------------------\n"
