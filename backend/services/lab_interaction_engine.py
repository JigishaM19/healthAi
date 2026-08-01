from typing import List, Dict, Any
from services.medication_database import DRUG_CONDITION_INTERACTIONS, DRUG_LAB_INTERACTIONS
from services.interaction_checker import normalize_med_name

def check_condition_medication_interactions(
    medication_list: List[str],
    conditions: List[str]
) -> List[Dict[str, Any]]:
    """
    Checks if any prescribed medication is contraindicated or risky for existing health conditions.
    """
    normalized_meds = [normalize_med_name(m) for m in (medication_list or [])]
    conditions_clean = [c.lower() for c in (conditions or [])]
    detected = []

    for rule in DRUG_CONDITION_INTERACTIONS:
        rule_drug = rule["drug"]
        rule_cond = rule["condition"]

        if rule_drug in normalized_meds:
            if any(rule_cond in c for c in conditions_clean):
                detected.append({
                    "severity": rule["severity"],
                    "interaction_type": "Condition-Medication",
                    "medication": rule_drug.title(),
                    "condition": rule_cond.title(),
                    "description": rule["description"],
                    "what_to_do": rule["what_to_do"],
                    "monitoring": rule["monitoring"]
                })

    return detected

def check_lab_medication_interactions(
    medication_list: List[str],
    lab_measurements: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Cross-references recent lab values (e.g. low potassium, high creatinine, high INR, low B12) against medications.
    """
    normalized_meds = [normalize_med_name(m) for m in (medication_list or [])]
    detected = []

    for lm in (lab_measurements or []):
        t_name = (lm.get("test_name") or lm.get("name") or "").lower()
        status = lm.get("status")

        for rule in DRUG_LAB_INTERACTIONS:
            rule_drug = rule["drug"]
            rule_lab = rule["lab"]
            rule_status = rule["lab_status"]

            if rule_drug in normalized_meds and rule_lab in t_name and status == rule_status:
                detected.append({
                    "severity": rule["severity"],
                    "interaction_type": "Lab-Medication",
                    "medication": rule_drug.title(),
                    "lab_test": lm.get("test_name") or lm.get("name"),
                    "lab_value": f"{lm.get('value')} {lm.get('unit','')}".strip(),
                    "lab_status": status,
                    "description": rule["description"],
                    "suggested_monitoring": rule["suggested_monitoring"]
                })

    return detected
