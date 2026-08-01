from typing import Dict, Any, List

def generate_workout_plan(
    age: int = 30,
    bmi: float = 24.5,
    goal: str = "lose_weight",
    activity_level: str = "sedentary",
    conditions: List[str] = None
) -> Dict[str, Any]:
    conditions_clean = [c.lower() for c in (conditions or [])]
    has_htn = any("hypertension" in c or "blood pressure" in c for c in conditions_clean)
    has_diabetes = any("diabet" in c for c in conditions_clean)
    has_joint = any("joint" in c or "arthritis" in c or "knee" in c for c in conditions_clean)

    if has_joint or age > 60:
        exercise_type = "Low Impact Aerobics & Joint Mobility"
        activities = ["Brisk Walking (30 mins daily)", "Water Aerobics / Swimming", "Gentle Chair Yoga & Stretching", "Stationary Cycling"]
        precautions = "Avoid high-impact jumping or heavy squatting; stop immediately if joint pain occurs."
    elif "gain" in (goal or "").lower() or "muscle" in (goal or "").lower():
        exercise_type = "Progressive Resistance Training"
        activities = ["Bodyweight Squats & Pushups (3 sets x 12 reps)", "Dumbbell Resistance Training (4 days/week)", "Post-workout Protein Intake within 30 mins"]
        precautions = "Maintain strict form; ensure 48 hours recovery for muscle groups."
    elif has_diabetes or has_htn:
        exercise_type = "Cardio & Post-Meal Glucose Control"
        activities = ["Post-meal 15-minute walks (3 times daily)", "Moderate Pace Brisk Walking (45 mins)", "Light Resistance Band Work"]
        precautions = "Stay hydrated; carry glucose tablets during workouts if on insulin or sulfonylureas."
    else: # Weight Loss / General Fitness
        exercise_type = "Fat Burn Cardio & Bodyweight Conditioning"
        activities = ["Brisk Walking / Jogging (45 mins daily)", "HIIT Circuit (20 mins, 3x/week)", "Bodyweight Core & Lower Body Circuit"]
        precautions = "Aim for 8,000 to 10,000 steps daily."

    return {
        "exercise_type": exercise_type,
        "recommended_activities": activities,
        "daily_step_target": 10000 if bmi >= 25 else 8000,
        "weekly_frequency": "5-6 Days / Week",
        "precautions": precautions
    }
