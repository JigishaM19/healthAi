from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from database import get_db
from models import User, HealthMemory
from auth import get_current_user
from services.nutrition_service import generate_personalized_diet_plan
from services.nutrition_memory_service import get_latest_nutrition_plan

router = APIRouter(tags=["AI Nutrition & Diet Planning System"])

@router.get("/nutrition/plan")
def get_nutrition_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = get_latest_nutrition_plan(db, current_user.id)
    if not plan:
        plan = generate_personalized_diet_plan(db, current_user.id)
    return plan

@router.post("/nutrition/generate")
def generate_new_nutrition_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return generate_personalized_diet_plan(db, current_user.id)

@router.get("/nutrition/history")
def get_nutrition_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    memories = db.query(HealthMemory).filter(
        HealthMemory.user_id == current_user.id,
        HealthMemory.memory_type == "nutrition_plan"
    ).order_by(HealthMemory.created_at.desc()).limit(10).all()
    return [m.metadata_json for m in memories if m.metadata_json]

@router.get("/nutrition/grocery-list")
def get_grocery_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = get_latest_nutrition_plan(db, current_user.id)
    if not plan:
        plan = generate_personalized_diet_plan(db, current_user.id)
    return plan.get("grocery_list", {})

@router.get("/nutrition/workout-plan")
def get_workout_plan_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = get_latest_nutrition_plan(db, current_user.id)
    if not plan:
        plan = generate_personalized_diet_plan(db, current_user.id)
    return plan.get("workout_plan", {})

@router.get("/nutrition/daily-routine")
def get_daily_routine_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = get_latest_nutrition_plan(db, current_user.id)
    if not plan:
        plan = generate_personalized_diet_plan(db, current_user.id)
    return plan.get("daily_routine", [])
