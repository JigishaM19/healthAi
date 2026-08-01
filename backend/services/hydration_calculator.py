def calculate_hydration_goal(weight_kg: float = 70.0, activity_level: str = "moderate") -> dict:
    base_l = weight_kg * 0.035
    act = (activity_level or "").lower()
    if "active" in act or "heavy" in act:
        extra = 0.75
    elif "light" in act:
        extra = 0.25
    else:
        extra = 0.5

    total = round(base_l + extra, 1)
    total = max(total, 2.5)

    return {
        "daily_target_liters": total,
        "daily_target_glasses": round(total * 4), # 250ml per glass
        "schedule": [
            "500 ml upon waking up (6:30 AM)",
            "500 ml before breakfast (7:30 AM)",
            "500 ml mid-morning (11:00 AM)",
            "500 ml 30 mins before lunch (1:00 PM)",
            "500 ml mid-afternoon (4:00 PM)",
            "500 ml 30 mins before dinner (7:30 PM)"
        ]
    }
