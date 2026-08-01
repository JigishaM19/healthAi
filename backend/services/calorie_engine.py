import math
from typing import Dict, Any, List

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculates Basal Metabolic Rate using the Mifflin-St Jeor Equation.
    Female: (10 * weight) + (6.25 * height) - (5 * age) - 161
    Male: (10 * weight) + (6.25 * height) - (5 * age) + 5
    """
    g = (gender or "male").lower()
    if "female" in g or "woman" in g:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    return max(bmr, 1000.0)

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculates Total Daily Energy Expenditure (TDEE) based on activity multiplier.
    """
    act = (activity_level or "sedentary").lower()
    if "light" in act:
        multiplier = 1.375
    elif "moderate" in act:
        multiplier = 1.55
    elif "extreme" in act or "very active" in act:
        multiplier = 1.9
    elif "active" in act or "heavy" in act:
        multiplier = 1.725
    else: # Sedentary
        multiplier = 1.2

    return bmr * multiplier

def calculate_nutrition_targets(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str = "lose_weight",
    conditions: List[str] = None
) -> Dict[str, Any]:
    """
    Calculates target calories, macronutrients (protein, carbs, fat, fiber), and hydration.
    Enforces safe minimum calorie thresholds (1200 kcal female, 1400 kcal male).
    Uses a 15-20% deficit for sustainable weight loss and 10-15% surplus for muscle gain.
    """
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    is_female = "female" in (gender or "").lower() or "woman" in (gender or "").lower()
    min_safe_calories = 1200.0 if is_female else 1400.0

    goal_clean = (goal or "").lower()
    if any(k in goal_clean for k in ["lose", "weight_loss", "fat_loss"]):
        # Sustainable 18% caloric deficit for safe fat loss (~1500-1700 kcal)
        target_calories = max(round(tdee * 0.82), min_safe_calories)
    elif any(k in goal_clean for k in ["gain", "muscle", "hypertrophy"]):
        # 12% caloric surplus for clean muscle building
        target_calories = round(tdee * 1.12)
    else: # Maintain weight / improve fitness / manage conditions
        target_calories = max(round(tdee), min_safe_calories)

    conditions_clean = [c.lower() for c in (conditions or [])]
    has_kidney = any("kidney" in c or "renal" in c for c in conditions_clean)
    has_diabetes = any("diabet" in c or "glucose" in c for c in conditions_clean)
    has_pcos = any("pcos" in c or "polycystic" in c for c in conditions_clean)
    has_thyroid = any("thyroid" in c for c in conditions_clean)

    # Macro distribution
    if has_kidney:
        # Controlled protein for kidney disease (0.8 g / kg body weight)
        protein_g = round(0.8 * weight_kg)
        protein_calories = protein_g * 4
        fat_pct = 0.30
        fat_g = round((target_calories * fat_pct) / 9)
        fat_calories = fat_g * 9
        carbs_calories = max(target_calories - protein_calories - fat_calories, 0)
        carbs_g = round(carbs_calories / 4)
    elif has_diabetes or has_pcos:
        # Controlled carbohydrates (35-40% carbs, 25-30% protein, 35% fat)
        protein_pct = 0.28
        carb_pct = 0.37
        fat_pct = 0.35
        protein_g = round((target_calories * protein_pct) / 4)
        carbs_g = round((target_calories * carb_pct) / 4)
        fat_g = round((target_calories * fat_pct) / 9)
    elif "gain" in goal_clean or "muscle" in goal_clean:
        # High protein for muscle building (2.0 g / kg)
        protein_g = round(min(2.0 * weight_kg, (target_calories * 0.35) / 4))
        fat_pct = 0.25
        fat_g = round((target_calories * fat_pct) / 9)
        carbs_g = round((target_calories - (protein_g * 4) - (fat_g * 9)) / 4)
    elif "lose" in goal_clean or "weight_loss" in goal_clean:
        # Fat loss: Protein ~ 1.8 g/kg
        protein_g = round(min(1.8 * weight_kg, (target_calories * 0.30) / 4))
        fat_pct = 0.30
        fat_g = round((target_calories * fat_pct) / 9)
        carbs_g = round((target_calories - (protein_g * 4) - (fat_g * 9)) / 4)
    else: # Balanced Maintenance
        protein_pct = 0.25
        carb_pct = 0.45
        fat_pct = 0.30
        protein_g = round((target_calories * protein_pct) / 4)
        carbs_g = round((target_calories * carb_pct) / 4)
        fat_g = round((target_calories * fat_pct) / 9)

    fiber_g = 30 if not is_female else 25
    if has_diabetes or has_pcos or "lose" in goal_clean:
        fiber_g += 5 # Additional dietary fiber for glycemic & satiety benefit

    bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "bmi": bmi,
        "target_calories": round(target_calories),
        "daily_calories": round(target_calories),
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "fiber_g": fiber_g,
        "protein_target": f"{protein_g}g",
        "carbohydrate_target": f"{carbs_g}g",
        "fat_target": f"{fat_g}g",
        "fiber_target": f"{fiber_g}g"
    }
