import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from models import User, HealthProfile, LabMeasurement
from services.calorie_engine import calculate_nutrition_targets
from services.diet_rules_engine import get_lab_aware_diet_rules
from services.meal_plan_generator import generate_7day_meal_plan, INDIAN_MEALS
from services.grocery_generator import generate_weekly_grocery_list
from services.workout_recommender import generate_workout_plan
from services.hydration_calculator import calculate_hydration_goal
from services.trend_analysis_service import get_tracked_trends
from services.nutrition_memory_service import save_nutrition_plan_memory
from services.timeline_service import create_event

def generate_personalized_diet_plan(db: Session, user_id: int, custom_query: Optional[str] = None) -> Dict[str, Any]:
    """
    Coordinates end-to-end AI Nutrition & Diet Planning:
    1. Fetches User Health Profile, Medical Conditions, Allergies, and Lab Measurements
    2. Runs Calorie & Macro Engine (Mifflin-St Jeor)
    3. Runs Lab-Aware Clinical Diet Rules Engine
    4. Generates 7-Day Indian Meal Plan
    5. Generates 9-Category Weekly Grocery Shopping List
    6. Generates Personalized Condition-Adapted Workout Plan
    7. Calculates Daily Hydration Goal & Schedule
    8. Persists to Health Memory & Health Timeline
    """
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()

    weight_kg = profile.weight_kg if profile and profile.weight_kg else 70.0
    height_cm = profile.height_cm if profile and profile.height_cm else 170.0
    age = profile.age if profile and profile.age else 30
    gender = profile.gender if profile and profile.gender else "Male"
    activity_level = profile.activity_level if profile and profile.activity_level else "sedentary"
    conditions = profile.conditions if profile and profile.conditions else []
    allergies = profile.allergies if profile and profile.allergies else []
    goals = profile.goals if profile and profile.goals else ["lose_weight"]
    diet_pref = profile.diet_type if profile and hasattr(profile, "diet_type") and profile.diet_type else "Vegetarian"

    # Fetch recent lab measurements & trends
    labs = db.query(LabMeasurement).filter(LabMeasurement.user_id == user_id).order_by(LabMeasurement.test_date.desc()).all()
    lab_list = [{"name": l.test_name, "value": l.value, "unit": l.unit, "status": l.status} for l in labs[:15]]
    lab_trends = get_tracked_trends(db, user_id)

    primary_goal = goals[0] if goals else "lose_weight"

    # 1. Calorie & Macro Engine
    targets = calculate_nutrition_targets(
        weight_kg=weight_kg,
        height_cm=height_cm,
        age=age,
        gender=gender,
        activity_level=activity_level,
        goal=primary_goal,
        conditions=conditions
    )

    # 2. Lab-Aware Rules Engine
    diet_rules = get_lab_aware_diet_rules(
        conditions=conditions,
        allergies=allergies,
        lab_measurements=lab_list,
        lab_trends=lab_trends
    )

    # 3. 7-Day Meal Plan
    meal_plan_7day = generate_7day_meal_plan(diet_preference=diet_pref, target_calories=targets["target_calories"])

    # 4. Weekly Grocery List
    grocery_list = generate_weekly_grocery_list(diet_preference=diet_pref)

    # 5. Workout Plan
    workout_plan = generate_workout_plan(
        age=age,
        bmi=targets["bmi"],
        goal=primary_goal,
        activity_level=activity_level,
        conditions=conditions
    )

    # 6. Hydration Schedule
    hydration = calculate_hydration_goal(weight_kg=weight_kg, activity_level=activity_level)

    # Meal options library for response standardization
    pref_key = "non_vegetarian" if any(k in diet_pref.lower() for k in ["non", "chicken", "egg", "fish"]) else "vegetarian"
    meal_options_db = INDIAN_MEALS.get(pref_key, INDIAN_MEALS["vegetarian"])

    # Daily Routine Schedule
    daily_routine = [
        {"time": "6:30 AM", "action": "Wake up + 500 ml Luke warm water with lemon"},
        {"time": "7:00 AM", "action": "30-45 mins Brisk Walk / Workout"},
        {"time": "8:00 AM", "action": f"Healthy Breakfast: {meal_plan_7day[0]['breakfast']}"},
        {"time": "11:00 AM", "action": f"Mid-Morning Snack: {meal_plan_7day[0]['mid_morning_snack']}"},
        {"time": "1:00 PM", "action": f"Balanced Lunch: {meal_plan_7day[0]['lunch']}"},
        {"time": "5:00 PM", "action": f"Evening Snack: {meal_plan_7day[0]['evening_snack']}"},
        {"time": "7:30 PM", "action": f"Light Dinner: {meal_plan_7day[0]['dinner']}"},
        {"time": "10:30 PM", "action": "Sleep (7.5 - 8 hours target)"}
    ]

    plan_result = {
        "user_id": user_id,
        "user_name": user.name if user else "Patient",
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "goal": primary_goal.replace("_", " ").title(),
        "goal_title": primary_goal.replace("_", " ").title(),
        "diet_preference": diet_pref,
        "daily_calories": targets["target_calories"],
        "calorie_target": targets["target_calories"],
        "target_calories": targets["target_calories"],

        # Macro Targets
        "protein_g": targets["protein_g"],
        "carbs_g": targets["carbs_g"],
        "fat_g": targets["fat_g"],
        "fiber_g": targets["fiber_g"],
        "protein_target": f"{targets['protein_g']}g",
        "carbohydrate_target": f"{targets['carbs_g']}g",
        "fat_target": f"{targets['fat_g']}g",
        "fiber_target": f"{targets['fiber_g']}g",

        # Hydration & Exercise
        "hydration_goal": hydration["hydration_target"],
        "hydration_liters": hydration["daily_target_liters"],
        "hydration": hydration,
        "exercise_target": workout_plan["exercise_type"],
        "sleep_target": "7.5 - 8.0 Hours / Night",

        # Options & Rules
        "meal_timing": daily_routine,
        "daily_routine": daily_routine,
        "breakfast_options": meal_options_db["breakfast"],
        "lunch_options": meal_options_db["lunch"],
        "dinner_options": meal_options_db["dinner"],
        "snack_options": meal_options_db["snack_morning"] + meal_options_db["snack_evening"],
        "foods_to_eat": diet_rules["foods_to_eat"],
        "foods_to_avoid": diet_rules["foods_to_avoid"],
        "clinical_notes": diet_rules["clinical_notes"],

        # Complete Structures
        "metrics": {
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "bmi": targets["bmi"],
            "bmr": targets["bmr"],
            "tdee": targets["tdee"]
        },
        "targets": targets,
        "diet_rules": diet_rules,
        "meal_plan": meal_plan_7day,
        "meal_plan_7day": meal_plan_7day,
        "grocery_list": grocery_list,
        "workout_plan": workout_plan
    }

    # Save to Health Memory
    try:
        save_nutrition_plan_memory(db, user_id, plan_result)
    except Exception as me:
        print("[NutritionService] Memory save error:", me)

    # Save to Health Timeline
    try:
        create_event(
            db=db,
            user_id=user_id,
            event_type="wellness",
            title=f"AI Nutrition Plan: {primary_goal.replace('_', ' ').title()}",
            summary=f"Personalized {diet_pref} diet plan created. Target: {targets['target_calories']} kcal/day ({targets['protein_g']}g Protein).",
            details={
                "target_calories": targets['target_calories'],
                "protein_g": targets['protein_g'],
                "diet_preference": diet_pref,
                "bmi": targets['bmi']
            }
        )
    except Exception as te:
        print("[NutritionService] Timeline event error:", te)

    return plan_result
