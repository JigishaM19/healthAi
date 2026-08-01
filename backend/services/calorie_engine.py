import math

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    # Mifflin-St Jeor Equation
    gender = (gender or "male").lower()
    if "female" in gender:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    return max(bmr, 1200.0)

def calculate_tdee(bmr: float, activity_level: str) -> float:
    act = (activity_level or "sedentary").lower()
    multiplier = 1.2 # Sedentary
    if "light" in act:
        multiplier = 1.375
    elif "moderate" in act:
        multiplier = 1.55
    elif "active" in act or "heavy" in act:
        multiplier = 1.725
    elif "very active" in act or "extreme" in act:
        multiplier = 1.9
    return bmr * multiplier

def calculate_nutrition_targets(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str = "lose_weight",
    conditions: list = None
) -> dict:
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    goal_clean = (goal or "").lower()
    if "lose" in goal_clean or "weight_loss" in goal_clean or "fat_loss" in goal_clean:
        target_calories = max(tdee - 500, 1200.0)
    elif "gain" in goal_clean or "muscle" in goal_clean:
        target_calories = tdee + 400
    else: # maintenance
        target_calories = tdee

    # Adjust for diabetes / PCOS
    conditions_clean = [c.lower() for c in (conditions or [])]
    if any("diabet" in c for c in conditions_clean):
        protein_pct = 0.25
        carb_pct = 0.40
        fat_pct = 0.35
    elif any("pcos" in c for c in conditions_clean) or any("thyroid" in c for c in conditions_clean):
        protein_pct = 0.30
        carb_pct = 0.35
        fat_pct = 0.35
    elif "gain" in goal_clean or "muscle" in goal_clean:
        protein_pct = 0.30
        carb_pct = 0.45
        fat_pct = 0.25
    else: # Balanced / Fat Loss
        protein_pct = 0.25
        carb_pct = 0.45
        fat_pct = 0.30

    protein_g = round((target_calories * protein_pct) / 4)
    carbs_g = round((target_calories * carb_pct) / 4)
    fat_g = round((target_calories * fat_pct) / 9)
    fiber_g = 30 if "female" not in (gender or "").lower() else 25

    # Hydration calculator (35ml per kg body weight + activity bonus)
    hydration_l = round((weight_kg * 0.035) + (0.5 if "active" in (activity_level or "").lower() else 0.0), 1)
    hydration_l = max(hydration_l, 2.0)

    bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "bmi": bmi,
        "target_calories": round(target_calories),
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "fiber_g": fiber_g,
        "hydration_l": hydration_l
    }
