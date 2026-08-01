import os
import httpx
from typing import Dict, Any, Optional

COLAB_AGENT_URL = os.getenv("COLAB_AGENT_URL", "")

EMERGENCY_KEYWORDS = ["chest pain", "can't breathe", "unconscious", "severe bleeding", "heart attack", "shortness of breath", "stroke"]
CRISIS_KEYWORDS = ["suicide", "kill myself", "self-harm", "want to die", "hopeless", "depressed"]

def route_triage(query: str, age: Optional[int] = None) -> Dict[str, str]:
    query_lower = query.lower()
    
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
