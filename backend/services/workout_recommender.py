from typing import Dict, Any, List

def generate_workout_plan(
    age: int = 30,
    bmi: float = 24.5,
    goal: str = "lose_weight",
    activity_level: str = "sedentary",
    conditions: List[str] = None
) -> Dict[str, Any]:
    """
    Generates a personalized, condition-adapted exercise & physical activity plan.
    Supports adaptations for Obesity, Diabetes, Hypertension, Thyroid, Arthritis/Joint Pain, Senior Age (>60), Pregnancy, etc.
    """
    conditions_clean = [c.lower() for c in (conditions or [])]
    
    has_joint = any(k in c for c in conditions_clean for k in ["joint", "arthritis", "knee", "back pain"])
    has_htn = any(k in c for c in conditions_clean for k in ["hypertension", "blood pressure", "bp"])
    has_diabetes = any(k in c for c in conditions_clean for k in ["diabet", "prediabet"])
    has_thyroid = any("thyroid" in c for c in conditions_clean)
    has_pregnancy = any("pregnan" in c for c in conditions_clean)
    is_senior = age >= 60

    if has_pregnancy:
        exercise_type = "Prenatal Low-Impact Wellness"
        cardio = "Prenatal Brisk Walking (20-30 mins daily at comfortable pace)"
        strength = "Light Resistance Band Upper Body Exercises (2x/week)"
        flexibility = "Prenatal Yoga & Pelvic Floor (Kegel) Exercises"
        duration = "30 Minutes / Day"
        cal_burned = "120 - 180 kcal"
        daily_steps = 6000
        precautions = "Avoid lying flat on back after 1st trimester; maintain hydration and avoid overheating."
    elif has_joint or is_senior:
        exercise_type = "Low Impact Aerobics & Joint Mobility"
        cardio = "Low-Impact Brisk Walking / Water Aerobics / Stationary Cycling"
        strength = "Bodyweight Squats to Chair & Wall Push-ups (2x/week)"
        flexibility = "Gentle Chair Yoga & Hamstring/Quadriceps Stretching"
        duration = "30-40 Minutes / Day"
        cal_burned = "150 - 220 kcal"
        daily_steps = 6000 if bmi >= 30 else 7500
        precautions = "Avoid high-impact jumping; discontinue immediately if acute joint pain occurs."
    elif "gain" in (goal or "").lower() or "muscle" in (goal or "").lower():
        exercise_type = "Progressive Resistance Hypertrophy Training"
        cardio = "Light Warm-up Walking (10 mins pre-workout)"
        strength = "Progressive Dumbbell / Barbell Compound Lifts (4 days/week: Squats, Bench, Rows, Overhead Press)"
        flexibility = "Dynamic Stretching pre-workout & Static Stretching post-workout"
        duration = "45-60 Minutes / Session"
        cal_burned = "300 - 450 kcal"
        daily_steps = 7500
        precautions = "Prioritize strict lifting form and consume post-workout protein within 45 mins."
    elif has_diabetes or has_htn:
        exercise_type = "Cardio & Post-Meal Glycemic Control"
        cardio = "15-minute walks immediately after main meals + 30 mins brisk walk"
        strength = "Light-to-Moderate Resistance Band & Bodyweight Exercises (3x/week)"
        flexibility = "Full Body Static Stretching & Deep Breathing Exercises"
        duration = "45 Minutes / Day"
        cal_burned = "220 - 320 kcal"
        daily_steps = 9000 if bmi >= 25 else 8000
        precautions = "Maintain hydration; carry fast-acting glucose tablets if taking insulin or sulfonylureas."
    elif bmi >= 30.0: # Obesity
        exercise_type = "Low-Impact Fat Burn & Caloric Expenditure"
        cardio = "Incline Treadmill Walking / Elliptical Cross Trainer (40 mins daily)"
        strength = "Seated Dumbbell Exercises & Cable Rows (3x/week)"
        flexibility = "Cat-Cow & Seated Hamstring Stretch"
        duration = "40-50 Minutes / Day"
        cal_burned = "250 - 380 kcal"
        daily_steps = 8500
        precautions = "Wear supportive athletic footwear; break walking into 20-min morning and evening sessions."
    else: # General Weight Loss / Fitness
        exercise_type = "Fat Burn Cardio & Bodyweight Conditioning"
        cardio = "Brisk Walking / Jogging / Cycling (45 mins daily)"
        strength = "Bodyweight Circuit: Squats, Push-ups, Lunges & Planks (3x/week)"
        flexibility = "Sun Salutations (Surya Namaskar) & Full Body Foam Rolling"
        duration = "45 Minutes / Day"
        cal_burned = "280 - 400 kcal"
        daily_steps = 10000
        precautions = "Strive for consistency; maintain 10,000 steps daily."

    return {
        "exercise_type": exercise_type,
        "daily_steps": daily_steps,
        "daily_step_target": daily_steps,
        "cardio_recommendation": cardio,
        "strength_training_target": strength,
        "flexibility_exercises": flexibility,
        "workout_duration": duration,
        "calories_burned_estimate": cal_burned,
        "weekly_activity_goal": "5-6 Days / Week",
        "recommended_activities": [cardio, strength, flexibility],
        "precautions": precautions
    }
