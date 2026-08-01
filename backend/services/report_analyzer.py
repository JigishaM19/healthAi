import os
import json
import httpx
from typing import Dict, Any, List, Optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

async def analyze_medical_document(
    extracted_text: str,
    document_type: str,
    structured_data: Dict[str, Any],
    user_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate clinical summary, abnormal findings, red flags, recommendations, and allergy/drug interaction warnings.
    """
    user_allergies = user_profile.get("allergies", []) if user_profile else []
    user_conditions = user_profile.get("conditions", []) if user_profile else []
    user_meds = user_profile.get("medications", []) if user_profile else []

    abnormal_values = []
    for lab in structured_data.get("lab_values", []):
        if lab.get("status") in ["Low", "High", "Abnormal"]:
            abnormal_values.append(lab)

    # 1. Allergy Conflict Check
    extracted_meds = structured_data.get("medicines", [])
    warnings = []

    for med in extracted_meds:
        med_name = med.get("name", "").lower()
        # Check penicillin cross-sensitivity
        for alg in user_allergies:
            alg_lower = alg.lower()
            if ("penicillin" in alg_lower or "amoxicillin" in alg_lower) and ("amoxicillin" in med_name or "penicillin" in med_name or "ampicillin" in med_name or "augmentin" in med_name):
                warnings.append(f"⚠️ ALLERGY CONFLICT WARNING: '{med['name']}' detected in document, but your health profile lists a '{alg}' allergy!")
            elif alg_lower in med_name:
                warnings.append(f"⚠️ ALLERGY CONFLICT WARNING: '{med['name']}' conflicts with your documented allergy to '{alg}'.")

    # 2. Call Groq AI if available
    if GROQ_API_KEY:
        try:
            prompt = f"""You are a clinical AI specialist analyzing a {document_type}.
Extracted Text:
\"\"\"
{extracted_text[:3000]}
\"\"\"
User Health Profile:
- Conditions: {', '.join(user_conditions) if user_conditions else 'None'}
- Allergies: {', '.join(user_allergies) if user_allergies else 'None'}
- Current Meds: {', '.join(user_meds) if user_meds else 'None'}

Provide a JSON output with:
{{
  "summary": "<Clear 2-sentence medical summary>",
  "abnormal_findings": ["<finding 1>", "<finding 2>"],
  "recommendations": ["<rec 1>", "<rec 2>"],
  "red_flags": ["<red flag 1>"],
  "personalized_advice": "<Advice connecting document findings to user profile>",
  "follow_up_actions": ["<action 1>"]
}}
ONLY return valid JSON."""

            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.2,
                        "response_format": {"type": "json_object"}
                    }
                )
                if response.status_code == 200:
                    parsed = json.loads(response.json()["choices"][0]["message"]["content"])
                    return {
                        "summary": parsed.get("summary", f"{document_type.replace('_', ' ').title()} successfully processed."),
                        "abnormal_findings": parsed.get("abnormal_findings", [f"{lab['name']} is {lab['status']}" for lab in abnormal_values]),
                        "recommendations": parsed.get("recommendations", ["Follow up with your primary physician", "Maintain regular hydration"]),
                        "red_flags": parsed.get("red_flags", ["Seek immediate care if acute symptoms arise"]),
                        "personalized_advice": parsed.get("personalized_advice", f"Document analyzed considering your health profile ({', '.join(user_conditions) if user_conditions else 'general wellness'})."),
                        "follow_up_actions": parsed.get("follow_up_actions", ["Schedule follow-up consultation"]),
                        "warnings": warnings,
                        "abnormal_values": abnormal_values
                    }
        except Exception as e:
            print(f"[ReportAnalyzer] Groq AI analysis error: {e}")

    # Fallback clinical analysis generator
    summary = f"Processed {document_type.replace('_', ' ').title()}. Extracted {len(extracted_meds)} medicines and {len(structured_data.get('lab_values', []))} laboratory markers."
    abnormal_findings = [f"{lab['name']}: {lab['value']} {lab['unit']} ({lab['status']} - Ref: {lab['reference']})" for lab in abnormal_values]
    
    recommendations = ["Consult with your attending physician regarding results", "Keep copy for permanent medical history"]
    red_flags = ["Seek immediate emergency care if chest pain, shortness of breath, or high fever occurs"]

    personalized_advice = "Document findings integrated with your personal health profile."
    if warnings:
        personalized_advice += " " + " ".join(warnings)

    return {
        "summary": summary,
        "abnormal_findings": abnormal_findings,
        "recommendations": recommendations,
        "red_flags": red_flags,
        "personalized_advice": personalized_advice,
        "follow_up_actions": ["Review findings with healthcare provider"],
        "warnings": warnings,
        "abnormal_values": abnormal_values
    }
