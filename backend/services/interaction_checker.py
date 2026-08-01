from typing import List, Dict, Any
from services.medication_database import MEDICATION_ALIASES, DRUG_DRUG_INTERACTIONS

def normalize_med_name(name: str) -> str:
    """Normalizes medication name to canonical generic form."""
    clean = (name or "").lower().strip()
    for brand, generic in MEDICATION_ALIASES.items():
        if brand in clean:
            return generic
    return clean

def check_drug_drug_interactions(medication_list: List[str]) -> List[Dict[str, Any]]:
    """
    Scans a list of medication strings for pairwise drug-drug interactions,
    duplicate therapies, and severe warnings.
    """
    normalized_map = {}
    for m in (medication_list or []):
        norm = normalize_med_name(m)
        if norm:
            normalized_map[norm] = m.strip()

    normalized_set = set(normalized_map.keys())
    detected_interactions = []

    for rule in DRUG_DRUG_INTERACTIONS:
        rule_drugs = set(rule["drugs"])
        if rule_drugs.issubset(normalized_set):
            matched_names = [normalized_map[d] for d in rule["drugs"]]
            detected_interactions.append({
                "severity": rule["severity"],
                "interaction_type": "Drug-Drug",
                "medications": matched_names,
                "category": rule["category"],
                "description": rule["description"],
                "what_to_do": rule["what_to_do"],
                "monitoring": rule["monitoring"]
            })

    return detected_interactions
