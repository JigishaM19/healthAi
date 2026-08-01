from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from models import HealthMemory
from services.health_memory_service import create_memory_entry

def save_nutrition_plan_memory(db: Session, user_id: int, plan_data: Dict[str, Any]) -> HealthMemory:
    title = f"AI Nutrition Plan: {plan_data.get('goal_title', 'Personalized Diet Plan')}"
    summary = (
        f"Calorie Target: {plan_data.get('targets', {}).get('target_calories')} kcal/day | "
        f"Protein: {plan_data.get('targets', {}).get('protein_g')}g | "
        f"Diet: {plan_data.get('diet_preference', 'Vegetarian')}"
    )

    return create_memory_entry(
        db=db,
        user_id=user_id,
        memory_type="nutrition_plan",
        title=title,
        summary=summary,
        source_type="nutrition_service",
        metadata_json=plan_data
    )

def get_latest_nutrition_plan(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
    mem = db.query(HealthMemory).filter(
        HealthMemory.user_id == user_id,
        HealthMemory.memory_type == "nutrition_plan"
    ).order_by(HealthMemory.created_at.desc()).first()

    if mem and mem.metadata_json:
        return mem.metadata_json
    return None
