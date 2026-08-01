from typing import List, Dict, Any
from services.medication_database import DRUG_FOOD_INTERACTIONS
from services.interaction_checker import normalize_med_name

def check_food_medication_interactions(
    medication_list: List[str],
    meal_plan: List[Dict[str, Any]] = None,
    foods_to_eat: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Analyzes medication list for food-medication interactions.
    Also cross-checks against active diet meal plans (e.g. spinach, grapefruit, dairy, tea).
    """
    normalized_meds = [normalize_med_name(m) for m in (medication_list or [])]
    detected_food_interactions = []

    # Flatten meal plan text if present
    plan_text_blob = ""
    if meal_plan:
        for day in meal_plan:
            plan_text_blob += f" {day.get('breakfast','')} {day.get('lunch','')} {day.get('dinner','')} {day.get('evening_snack','')}"
    if foods_to_eat:
        plan_text_blob += " " + " ".join(foods_to_eat)
    plan_text_blob = plan_text_blob.lower()

    for rule in DRUG_FOOD_INTERACTIONS:
        rule_drug = rule["drug"]
        rule_food = rule["food"]

        if rule_drug in normalized_meds:
            # Check if this food is present in the meal plan or general rules
            in_active_plan = rule_food in plan_text_blob or any(fa.lower() in plan_text_blob for fa in rule["foods_to_avoid"])
            
            severity = rule["severity"]
            if in_active_plan and severity == "Moderate":
                severity = "High" # Escalate severity if food is explicitly in user's meal plan!

            detected_food_interactions.append({
                "severity": severity,
                "interaction_type": "Food-Medication",
                "medication": rule_drug.title(),
                "conflicting_food": rule_food.title(),
                "in_active_meal_plan": in_active_plan,
                "description": rule["description"],
                "foods_to_avoid": rule["foods_to_avoid"],
                "foods_allowed": rule["foods_allowed"],
                "timing_advice": rule["timing_advice"]
            })

    return detected_food_interactions
