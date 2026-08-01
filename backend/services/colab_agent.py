import os
import httpx
from typing import Dict, Any, Optional

COLAB_AGENT_URL = os.getenv("COLAB_AGENT_URL", "")

EMERGENCY_KEYWORDS = ["chest pain", "can't breathe", "unconscious", "severe bleeding", "heart attack", "shortness of breath", "stroke"]
CRISIS_KEYWORDS = ["suicide", "kill myself", "self-harm", "want to die", "hopeless", "depressed"]
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

def route_triage(query: str, age: Optional[int] = None) -> Dict[str, str]:
    query_lower = (query or "").lower()

    if any(kw in query_lower for kw in CRISIS_KEYWORDS):
        return {
            "ward": "mental_health",
            "reasoning": "Crisis keyword detected — routed immediately to Mental Health Ward for safety.",
            "assigned_doctor": "Dr. Sarah Jenkins (Psychiatry Lead)"
        }
    elif any(kw in query_lower for kw in EMERGENCY_KEYWORDS):
        return {
            "ward": "emergency",
            "reasoning": "Emergency keyword detected — routed immediately to Emergency Ward for urgent care.",
            "assigned_doctor": "Dr. Marcus Vance (ER Trauma Specialist)"
        }
    elif any(kw in query_lower for kw in NUTRITION_KEYWORDS):
        return {
            "ward": "nutrition_dietetics",
            "reasoning": "Nutrition, diet, weight loss, or lifestyle query detected — routed to Clinical Dietetics.",
            "assigned_doctor": "Clinical Dietitian & Sports Nutritionist"
        }
    else:
        return {
            "ward": "general",
            "reasoning": "Standard health consultation query classified as General Practice.",
            "assigned_doctor": "Dr. Elena Rostova (General Internal Medicine)"
        }

async def query_colab_endpoint(query: str, profile_data: Dict[str, Any], history: list) -> Optional[Dict[str, Any]]:
    if not COLAB_AGENT_URL:
        return None

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                COLAB_AGENT_URL.rstrip('/') + "/chat",
                json={
                    "message": query,
                    "profile": profile_data,
                    "history": history
                }
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        print(f"[ColabAgent] Failed to query remote endpoint: {e}")
    return None
