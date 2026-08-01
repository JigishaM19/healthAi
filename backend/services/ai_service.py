import os
import json
import httpx
from typing import Dict, Any, List, Optional
from services.colab_agent import route_triage, query_colab_endpoint

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

NUTRITION_KEYWORDS = [
    "lose weight", "weight loss", "gain weight", "muscle gain", "fat loss",
    "diet", "diet plan", "meal plan", "calories", "calorie target", "calorie deficit",
    "macro", "macros", "protein", "carbohydrates", "carbs", "fats", "fat", "fiber",
    "hydration", "water intake", "what to eat", "what should i eat", "food to eat",
    "food to avoid", "grocery list", "grocery", "workout", "exercise", "daily routine",
    "diabetes diet", "diabetic diet", "thyroid diet", "pcos diet", "pcos",
    "cholesterol", "high cholesterol", "hypertension", "blood pressure diet",
    "fatty liver", "liver diet", "kidney diet", "high protein", "low carb",
    "vegetarian", "vegan", "jain diet", "keto", "7-day meal plan", "7 day meal plan",
    "7 day plan", "dietitian", "nutrition", "nutritionist", "explain my report",
    "suggest food", "food according to report", "fitness", "healthy eating",
    "what should i eat daily", "food", "meals", "meal", "eating", "eat"
]

MEDICATION_KEYWORDS = [
    "take together", "can i take", "interaction", "medicine", "medication",
    "drug", "pill", "prescription", "side effect", "timing", "schedule",
    "metformin", "levothyroxine", "amlodipine", "aspirin", "warfarin",
    "ibuprofen", "naproxen", "paracetamol", "statin", "atorvastatin",
    "drink milk with", "grapefruit", "spinach with", "empty stomach",
    "with food", "dangerous together", "safe to take", "take my medicines"
]

def is_nutrition_intent(message: str) -> bool:
    """Detects whether a user message expresses nutrition, diet, food, or lifestyle intent."""
    msg = (message or "").lower()
    return any(k in msg for k in NUTRITION_KEYWORDS)

def is_medication_intent(message: str) -> bool:
    """Detects whether a user message expresses medication, drug safety, interaction, or timing intent."""
    msg = (message or "").lower()
    return any(k in msg for k in MEDICATION_KEYWORDS)

def generate_dietitian_guidance(
    user_message: str,
    profile_data: Optional[Dict[str, Any]],
    n_plan: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Constructs a comprehensive, personalized AI Dietitian response with macros,
    7-day Indian meal plan, 9-group grocery list, hydration schedule, and workout targets.
    """
    age = profile_data.get("age", 30) if profile_data else 30
    gender = profile_data.get("gender", "Unspecified") if profile_data else "Unspecified"
    height = profile_data.get("height_cm", 170.0) if profile_data else 170.0
    weight = profile_data.get("weight_kg", 70.0) if profile_data else 70.0
    conditions = profile_data.get("conditions", []) if profile_data else []
    allergies = profile_data.get("allergies", []) if profile_data else []

    t = n_plan.get("targets", {})
    t_cal = t.get("target_calories", n_plan.get("daily_calories", 1600))
    p_g = t.get("protein_g", 100)
    c_g = t.get("carbs_g", 150)
    f_g = t.get("fat_g", 50)
    fib_g = t.get("fiber_g", 30)
    bmi = n_plan.get("metrics", {}).get("bmi", 24.2)
    bmr = n_plan.get("metrics", {}).get("bmr", 1500)
    tdee = n_plan.get("metrics", {}).get("tdee", 1900)

    rules = n_plan.get("diet_rules", {})
    foods_eat = rules.get("foods_to_eat", n_plan.get("foods_to_eat", []))
    foods_avoid = rules.get("foods_to_avoid", n_plan.get("foods_to_avoid", []))
    clinical_notes = rules.get("clinical_notes", n_plan.get("clinical_notes", []))

    meal_7day = n_plan.get("meal_plan_7day", n_plan.get("meal_plan", []))
    grocery = n_plan.get("grocery_list", {})
    workout = n_plan.get("workout_plan", {})
    hydration = n_plan.get("hydration", {})
    hydration_text = n_plan.get("hydration_goal", f"{hydration.get('daily_target_liters', 3.0)} Liters/day")

    # Format 7-Day Meal Plan
    meal_lines = []
    for day_item in meal_7day:
        d_name = day_item.get("day", "Day")
        bf = day_item.get("breakfast", "")
        sn1 = day_item.get("mid_morning_snack", day_item.get("morning_snack", ""))
        ln = day_item.get("lunch", "")
        sn2 = day_item.get("evening_snack", "")
        dn = day_item.get("dinner", "")
        meal_lines.append(
            f"**{d_name}**:\n"
            f"  - *Breakfast*: {bf}\n"
            f"  - *Mid-Morning*: {sn1}\n"
            f"  - *Lunch*: {ln}\n"
            f"  - *Evening Snack*: {sn2}\n"
            f"  - *Dinner*: {dn}"
        )
    meal_plan_markdown = "\n\n".join(meal_lines)

    # Format Grocery List
    grocery_lines = []
    for category, items in grocery.items():
        if items:
            grocery_lines.append(f"**{category}**: {', '.join(items[:6])}")
    grocery_markdown = "\n".join(grocery_lines)

    # Format Clinical Notes
    c_note_str = " ".join(clinical_notes) if clinical_notes else "Maintain balanced nutrition, adequate hydration, and regular exercise."

    reply_markdown = f"""## 🥗 HealthAI Personal AI Dietitian Assessment & Plan

Based on your personal medical profile (**Age**: {age}, **Gender**: {gender}, **Height**: {height} cm, **Weight**: {weight} kg, **BMI**: {bmi}, **Goal**: {n_plan.get('goal', 'Wellness')}) and your medical conditions ({', '.join(conditions) if conditions else 'None reported'}):

### 📊 Daily Caloric & Macronutrient Targets
- 🎯 **Daily Calorie Target**: **{t_cal} kcal/day** *(BMR: {bmr} kcal | TDEE: {tdee} kcal)*
- 🥩 **Protein**: **{p_g}g**
- 🌾 **Carbohydrates**: **{c_g}g**
- 🥑 **Fats**: **{f_g}g**
- 🥬 **Dietary Fiber**: **{fib_g}g/day**
- 💧 **Hydration Goal**: **{hydration_text}**

---

### 🥗 Foods to Include & Eat
{chr(10).join(['- ' + f for f in foods_eat[:8]])}

### 🚫 Foods to Avoid or Limit
{chr(10).join(['- ' + f for f in foods_avoid[:8]])}

---

### 📅 Complete 7-Day Personalized Meal Plan

{meal_plan_markdown}

---

### 🛒 Categorized Weekly Grocery Shopping List
{grocery_markdown}

---

### 🏃 Personalized Exercise & Workout Recommendation
- **Exercise Protocol**: {workout.get('exercise_type', 'Condition-Adapted Fitness')}
- **Daily Steps Goal**: **{workout.get('daily_steps', workout.get('daily_step_target', 8000))} steps/day**
- **Cardio Target**: {workout.get('cardio_recommendation', 'Brisk Walking (30-45 mins)')}
- **Strength Training**: {workout.get('strength_training_target', 'Bodyweight / Resistance Band Exercises')}
- **Flexibility & Mobility**: {workout.get('flexibility_exercises', 'Stretching / Gentle Yoga')}
- **Duration & Calorie Burn**: {workout.get('workout_duration', '45 mins/day')} *(Est. {workout.get('calories_burned_estimate', '250-350 kcal')} burned)*
- ⚠️ **Precautions**: {workout.get('precautions', 'Stay hydrated and listen to your body.')}

---

### ⏰ Recommended Daily Routine
- **6:30 AM**: Wake up + 500 ml Luke warm water with lemon
- **7:00 AM**: 30-45 mins Brisk Walk / Workout
- **8:00 AM**: Healthy Breakfast
- **11:00 AM**: Mid-Morning Fruit + Almonds / Green Tea
- **1:00 PM**: Balanced Lunch
- **5:00 PM**: Evening Tea / Buttermilk + Roasted Makhana
- **7:30 PM**: Light Dinner
- **10:30 PM**: Sleep (7.5 - 8 hours target)

---

> 🩺 **Medical & Clinical Note**:
> {c_note_str}
> *Disclaimer: This plan is generated for clinical educational and wellness support. Please consult your primary care physician or registered dietitian before embarking on restrictive diets or high-intensity exercise routines, especially if managing underlying medical conditions.*"""

    analysis_card = {
        "possible_causes": [
            f"Caloric & macronutrient balance for {n_plan.get('goal', 'health optimization')}",
            f"Metabolic adaptation for BMI {bmi} ({'Overweight/Obesity' if bmi >= 25 else 'Healthy weight'})",
            f"Condition-aware dietary requirement ({', '.join(conditions) if conditions else 'General wellness'})"
        ],
        "recommended_actions": [
            f"Target daily caloric intake of {t_cal} kcal/day with {p_g}g protein",
            f"Maintain hydration of {hydration_text} and hit {workout.get('daily_steps', 8000)} daily steps",
            "Follow the 7-day Indian meal plan and grocery list provided"
        ],
        "warning_signs": [
            "Dizziness, lethargy, or extreme hunger from sudden caloric drops",
            "Severe joint or muscle discomfort during workouts",
            "Hypoglycemia symptoms (shakiness, sweating) if taking diabetic medications"
        ],
        "personalized_advice": f"Plan customized for user (Age: {age}, Weight: {weight}kg, Goal: {n_plan.get('goal')}). {c_note_str}",
        "confidence": 0.95,
        "ward": "nutrition_dietetics",
        "assigned_doctor": "Clinical Dietitian & Sports Nutritionist"
    }

    return {
        "reply": reply_markdown,
        "analysis": analysis_card
    }

def generate_medication_guidance(
    user_message: str,
    profile_data: Optional[Dict[str, Any]],
    m_report: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Constructs a comprehensive, personalized AI Medication Safety response with
    drug-drug, food-medication, condition, and lab interaction warnings + daily timing schedule.
    """
    meds = m_report.get("medications_analyzed", [])
    severity = m_report.get("overall_severity", "Safe")
    dd = m_report.get("drug_drug_interactions", [])
    fd = m_report.get("food_interactions", [])
    cd = m_report.get("condition_interactions", [])
    ld = m_report.get("lab_interactions", [])
    sched = m_report.get("medication_schedule", [])

    dd_lines = []
    for item in dd:
        dd_lines.append(
            f"  - ⚠️ **[{item['severity']} Risk] {', '.join(item['medications'])}**: {item['description']}\n"
            f"    - *Action*: {item['what_to_do']}\n"
            f"    - *Monitor*: {', '.join(item['monitoring'])}"
        )

    fd_lines = []
    for item in fd:
        fd_lines.append(
            f"  - 🥛 **[{item['severity']} Risk] {item['medication']} + {item['conflicting_food']}**: {item['description']}\n"
            f"    - *Timing Advice*: {item['timing_advice']}\n"
            f"    - *Foods to Avoid*: {', '.join(item['foods_to_avoid'][:4])}"
        )

    cd_lines = []
    for item in cd:
        cd_lines.append(
            f"  - 🩺 **[{item['severity']} Risk] {item['medication']} & {item['condition']}**: {item['description']}\n"
            f"    - *Action*: {item['what_to_do']}"
        )

    ld_lines = []
    for item in ld:
        ld_lines.append(
            f"  - 🔬 **[{item['severity']} Risk] {item['medication']} & Lab {item['lab_test']} ({item['lab_value']})**: {item['description']}\n"
            f"    - *Suggested Action*: {item['suggested_monitoring']}"
        )

    sched_lines = []
    for entry in sched:
        sched_lines.append(
            f"  - ⏰ **{entry['time']}**: **{entry['medication']}** ({entry['meal_relation']})\n"
            f"    - *Guideline*: {entry['spacing_rule']}"
        )

    reply_markdown = f"""## 💊 HealthAI Medication Safety Intelligence Report

Based on your active medications ({', '.join(meds) if meds else 'None reported'}) and your medical profile:

### 🛡️ Overall Safety Risk Severity: **{severity.upper()}**

---

### 🚨 Drug-Drug Interactions
{chr(10).join(dd_lines) if dd_lines else "✅ *No direct drug-drug interactions detected among your current medications.*"}

---

### 🥦 Food & Dietary Medication Conflicts
{chr(10).join(fd_lines) if fd_lines else "✅ *No critical food-medication conflicts detected.*"}

---

### 🩺 Health Condition & Lab Considerations
{chr(10).join(cd_lines + ld_lines) if (cd_lines or ld_lines) else "✅ *No condition or lab contraindications detected.*"}

---

### ⏰ Optimized Daily Medication Schedule
{chr(10).join(sched_lines) if sched_lines else "✅ *No active medications requiring specific spacing.*"}

---

> ⚠️ **Medical Safety Disclaimer**:
> {m_report.get('safety_disclaimer')}
> *Do not discontinue or change any medication without consulting your healthcare professional.*"""

    analysis_card = {
        "possible_causes": [
            f"Pharmacological risk evaluation for {len(meds)} active medications",
            f"Cytochrome P450 and gastrointestinal binding interaction audit",
            f"Condition-medication compatibility ({severity} overall risk)"
        ],
        "recommended_actions": [
            "Review the optimized daily medication schedule and spacing guidelines",
            "Avoid high-risk food combinations highlighted in your safety report",
            "Consult your pharmacist or physician before adding new over-the-counter drugs"
        ],
        "warning_signs": [
            "Unexplained bruising, bleeding gums, or dark stools",
            "Sudden muscle weakness, dizziness, or irregular heartbeat",
            "Signs of allergic reaction (rash, facial swelling, trouble breathing)"
        ],
        "personalized_advice": f"Medication safety audit completed. Overall Severity: {severity}. Always discuss prescription changes with your doctor.",
        "confidence": 0.96,
        "ward": "pharmacology",
        "assigned_doctor": "Clinical Pharmacologist & Medication Safety Specialist"
    }

    return {
        "reply": reply_markdown,
        "analysis": analysis_card
    }

async def generate_health_guidance(
    user_message: str,
    profile_data: Optional[Dict[str, Any]],
    conversation_history: List[Dict[str, str]],
    memory_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate context-aware AI health guidance incorporating the user's profile and historical health memory.
    """
    # 0a. Check Medication Intent First
    if is_medication_intent(user_message):
        try:
            from database import SessionLocal
            from services.medication_safety_service import run_medication_safety_audit
            db = SessionLocal()
            try:
                user_id = profile_data.get("user_id", 1) if profile_data else 1
                m_report = run_medication_safety_audit(db, user_id)
                return generate_medication_guidance(user_message, profile_data, m_report)
            finally:
                db.close()
        except Exception as me:
            print("[AIService] Medication safety guidance fallback note:", me)

    # 0b. Check Nutrition Intent Second
    if is_nutrition_intent(user_message):
        try:
            from database import SessionLocal
            from services.nutrition_service import generate_personalized_diet_plan
            db = SessionLocal()
            try:
                user_id = profile_data.get("user_id", 1) if profile_data else 1
                n_plan = generate_personalized_diet_plan(db, user_id, user_message)
                return generate_dietitian_guidance(user_message, profile_data, n_plan)
            finally:
                db.close()
        except Exception as e:
            print("[AIService] Direct dietitian guidance fallback note:", e)

    # 1. Run Colab Agent Remote Endpoint if configured
    if profile_data:
        remote_res = await query_colab_endpoint(user_message, profile_data, conversation_history)
        if remote_res and "reply" in remote_res and "analysis" in remote_res:
            return remote_res

    # 2. Extract profile context
    age = profile_data.get("age", 30) if profile_data else 30
    gender = profile_data.get("gender", "Unspecified") if profile_data else "Unspecified"
    conditions = profile_data.get("conditions", []) if profile_data else []
    medications = profile_data.get("medications", []) if profile_data else []
    allergies = profile_data.get("allergies", []) if profile_data else []
    goals = profile_data.get("goals", []) if profile_data else []
    stress = profile_data.get("stress_level", 3) if profile_data else 3
    mood = profile_data.get("mood", "Calm") if profile_data else "Calm"

    triage = route_triage(user_message, age)

    # 3. If Groq API Key is available, use llama-3.3-70b-versatile via Groq HTTP API
    if GROQ_API_KEY:
        try:
            mem_text = f"\n{memory_context}" if memory_context else ""
            system_prompt = f"""You are HealthAI, an advanced clinical assistant.
User Profile:
- Age: {age}, Gender: {gender}
- Existing Conditions: {', '.join(conditions) if conditions else 'None reported'}
- Medications: {', '.join(medications) if medications else 'None reported'}
- Allergies: {', '.join(allergies) if allergies else 'None reported'}
- Health Goals: {', '.join(goals) if goals else 'General wellness'}
- Mood/Stress: {mood} (Stress score: {stress}/5){mem_text}

Respond with a JSON object containing EXACTLY:
{{
  "reply": "<Detailed empathetic clinical explanation tailored to user>",
  "possible_causes": ["<cause 1>", "<cause 2>", "<cause 3>"],
  "recommended_actions": ["<action 1>", "<action 2>", "<action 3>"],
  "warning_signs": ["<red flag 1>", "<red flag 2>"],
  "personalized_advice": "<Specific advice incorporating their conditions/medications/goals>",
  "confidence": 0.88
}}
ONLY return valid JSON."""

            messages = [{"role": "system", "content": system_prompt}]
            for msg in conversation_history[-4:]:
                messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            messages.append({"role": "user", "content": user_message})

            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "temperature": 0.3,
                        "response_format": {"type": "json_object"}
                    }
                )
                if response.status_code == 200:
                    raw_content = response.json()["choices"][0]["message"]["content"]
                    parsed = json.loads(raw_content)
                    return {
                        "reply": parsed.get("reply", "Here is your health analysis based on your symptoms."),
                        "analysis": {
                            "possible_causes": parsed.get("possible_causes", ["Viral infection", "Stress/Fatigue", "Mild inflammation"]),
                            "recommended_actions": parsed.get("recommended_actions", ["Hydrate adequately", "Rest", "Monitor symptoms"]),
                            "warning_signs": parsed.get("warning_signs", ["Chest pain", "Difficulty breathing", "High fever > 103°F"]),
                            "personalized_advice": parsed.get("personalized_advice", f"Because you reported {conditions[0] if conditions else 'general health goals'}, maintain your regular wellness routine."),
                            "confidence": float(parsed.get("confidence", 0.87)),
                            "ward": triage["ward"],
                            "assigned_doctor": triage["assigned_doctor"]
                        }
                    }
        except Exception as e:
            print(f"[AIService] Groq API call failed or timed out: {e}")

    # 4. Built-in High Quality Context-Aware Triage Engine (Fallback / Default)
    query_lower = user_message.lower()

    possible_causes = ["Viral upper respiratory infection", "Environmental or seasonal allergies", "Dehydration & muscle tension"]
    recommended_actions = ["Maintain adequate hydration (2.5L+ daily)", "Get at least 7.5 hours of restorative sleep", "Monitor body temperature and symptoms closely"]
    warning_signs = ["Sudden severe chest pain or pressure", "Shortness of breath or rapid labored breathing", "High fever persisting over 48 hours", "Confusion or severe dizziness"]

    if "fever" in query_lower or "headache" in query_lower or "cold" in query_lower:
        possible_causes = ["Viral infection (flu or common cold)", "Sinusitis / allergic rhinitis", "Physical exhaustion & mild dehydration"]
        recommended_actions = ["Rest in a well-ventilated room", "Increase fluid intake (warm teas, electrolyte solution)", "Use over-the-counter fever reducers if appropriate"]
    elif "stomach" in query_lower or "nausea" in query_lower or "pain" in query_lower:
        possible_causes = ["Mild gastroenteritis or dietary irritation", "Acid reflux / indigestion", "Stress-induced visceral tension"]
        recommended_actions = ["Eat light, bland foods (toast, bananas, rice)", "Avoid caffeine, spicy, or greasy meals", "Sip ginger or peppermint tea"]
    elif "anxious" in query_lower or "stress" in query_lower or "sleep" in query_lower:
        possible_causes = ["Elevated cortisol & nervous system overload", "Sleep deprivation or disruption of circadian rhythm", "Workload or lifestyle fatigue"]
        recommended_actions = ["Practice 4-7-8 deep breathing exercises", "Limit screen exposure 1 hour before bedtime", "Engage in light 15-minute evening walks"]

    advice_parts = []
    if conditions:
        advice_parts.append(f"Because you reported existing conditions ({', '.join(conditions)}), ensure your vital signs remain stable and monitor for any sudden changes.")
    if medications:
        advice_parts.append(f"Verify that any over-the-counter remedies do not interact with your current medications ({', '.join(medications)}).")
    if allergies:
        advice_parts.append(f"Remember your documented allergies ({', '.join(allergies)}) when taking any medication or herbal supplement.")
    if goals:
        advice_parts.append(f"To support your health goals ({', '.join(goals)}), prioritize hydration and consistency.")

    if not advice_parts:
        advice_parts.append("Based on your profile, maintain balanced nutrition, regular hydration, and consistent sleeping patterns.")

    personalized_advice = " ".join(advice_parts)

    reply_text = (
        f"Thank you for sharing your symptoms. Based on your description ('{user_message}') "
        f"and your personal health profile (Age: {age}, Gender: {gender}), I have analyzed your condition.\n\n"
        f"Triage Ward: {triage['ward'].upper().replace('_', ' ')} | Assigned Medical Specialist: {triage['assigned_doctor']}.\n\n"
        f"Key Assessment:\n{personalized_advice}\n\n"
        f"Please review the detailed possible causes, recommended actions, and red flag warning signs below."
    )

    return {
        "reply": reply_text,
        "analysis": {
            "possible_causes": possible_causes,
            "recommended_actions": recommended_actions,
            "warning_signs": warning_signs,
            "personalized_advice": personalized_advice,
            "confidence": 0.86 if triage["ward"] == "general" else 0.94,
            "ward": triage["ward"],
            "assigned_doctor": triage["assigned_doctor"]
        }
    }
