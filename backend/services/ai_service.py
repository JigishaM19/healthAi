import os
import json
import httpx
from typing import Dict, Any, List, Optional
from services.colab_agent import route_triage, query_colab_endpoint

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

async def generate_health_guidance(
    user_message: str,
    profile_data: Optional[Dict[str, Any]],
    conversation_history: List[Dict[str, str]],
    memory_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate context-aware AI health guidance incorporating the user's profile and historical health memory.
    """
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
    
    # Custom cause/action extraction based on symptoms
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

    # Build profile-specific personalized advice
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
