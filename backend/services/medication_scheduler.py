from typing import List, Dict, Any
from services.medication_database import MEDICATION_TIMING_RULES
from services.interaction_checker import normalize_med_name

def generate_medication_schedule(medication_list: List[str]) -> List[Dict[str, Any]]:
    """
    Generates a chronologically sorted daily medication schedule with exact timing,
    meal relations, and safety spacing guidelines.
    """
    schedule_entries = []

    for m in (medication_list or []):
        norm = normalize_med_name(m)
        rule = MEDICATION_TIMING_RULES.get(norm)

        if rule:
            schedule_entries.append({
                "medication": m.strip().title(),
                "time": rule["best_time"],
                "meal_relation": rule["meal_relation"],
                "spacing_rule": rule["spacing_rule"]
            })
        else:
            schedule_entries.append({
                "medication": m.strip().title(),
                "time": "8:00 AM",
                "meal_relation": "With or after breakfast",
                "spacing_rule": "Take consistently at the same time each day with a full glass of water."
            })

    # Sort schedule by time string
    def parse_time_key(item):
        t_str = item["time"].split("&")[0].strip()
        is_pm = "PM" in t_str
        parts = t_str.replace("AM", "").replace("PM", "").strip().split(":")
        hr = int(parts[0]) if parts[0].isdigit() else 8
        if is_pm and hr < 12:
            hr += 12
        elif not is_pm and hr == 12:
            hr = 0
        mn = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return hr * 60 + mn

    schedule_entries.sort(key=parse_time_key)
    return schedule_entries
