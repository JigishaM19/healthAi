from typing import List, Dict, Any

def get_lab_aware_diet_rules(
    conditions: List[str] = None,
    allergies: List[str] = None,
    lab_measurements: List[Dict[str, Any]] = None,
    lab_trends: Dict[str, Any] = None
) -> Dict[str, Any]:
    foods_to_eat = set()
    foods_to_avoid = set()
    clinical_notes = []

    conditions_clean = [c.lower() for c in (conditions or [])]
    allergies_clean = [a.lower() for a in (allergies or [])]
    
    # 1. Check Diabetes / High Glucose / HbA1c
    has_diabetes = any("diabet" in c for c in conditions_clean)
    has_high_glucose = False
    for lm in (lab_measurements or []):
        t_name = (lm.get("test_name") or lm.get("name") or "").lower()
        if ("glucose" in t_name or "hba1c" in t_name) and lm.get("status") in ["High", "Critical"]:
            has_high_glucose = True

    if has_diabetes or has_high_glucose:
        foods_to_eat.update(["Oats", "Moong Dal", "Bitter Gourd (Karela)", "Fenugreek (Methi)", "Sprouts", "Chia Seeds", "Cinnamon", "Green Leafy Vegetables"])
        foods_to_avoid.update(["Sugary Drinks", "White Rice", "Bakery Goods", "Fruit Juices", "Refined Flour (Maida)", "Sweets & Desserts", "Deep-fried Snacks"])
        clinical_notes.append("Glycemic Control: Emphasize low-GI complex carbs paired with lean protein to prevent glucose spikes.")

    # 2. Check High Cholesterol / High LDL / Triglycerides
    has_high_chol = any("cholesterol" in c or "lipid" in c for c in conditions_clean)
    has_high_ldl = False
    for lm in (lab_measurements or []):
        t_name = (lm.get("test_name") or lm.get("name") or "").lower()
        if ("cholesterol" in t_name or "ldl" in t_name or "triglyceride" in t_name) and lm.get("status") in ["High", "Critical"]:
            has_high_ldl = True

    if has_high_chol or has_high_ldl:
        foods_to_eat.update(["Rolled Oats", "Flaxseeds", "Walnuts", "Garlic", "Avocado", "Apples", "Legumes", "Extra Virgin Olive Oil"])
        foods_to_avoid.update(["Butter & Ghee (in excess)", "Red Meat", "Full-fat Dairy", "Fried Foods", "Trans Fats", "Processed Meats"])
        clinical_notes.append("Cardiovascular & Lipid Control: Increase soluble fiber (5-10g/day) to lower LDL cholesterol naturally.")

    # 3. Check High Blood Pressure / Hypertension
    has_htn = any("hypertension" in c or "blood pressure" in c for c in conditions_clean)
    if has_htn:
        foods_to_eat.update(["Bananas", "Spinach", "Beetroot Juice", "Pomegranates", "Unsalted Seeds", "Coconut Water", "Garlic"])
        foods_to_avoid.update(["High Sodium Pickles", "Papad", "Processed Soups", "Salty Snacks", "Canned Foods", "Excess Salt"])
        clinical_notes.append("DASH Protocol: Restrict sodium to < 2,000 mg/day; boost potassium-rich vegetables.")

    # 4. Check Thyroid (Hypothyroidism)
    has_thyroid = any("thyroid" in c for c in conditions_clean)
    if has_thyroid:
        foods_to_eat.update(["Brazil Nuts (Selenium)", "Eggs", "Yogurt", "Pumpkin Seeds", "Cooked Vegetables"])
        foods_to_avoid.update(["Raw Goitrogens (Raw Cabbage, Raw Broccoli)", "Soy Products", "Excessive Caffeine"])
        clinical_notes.append("Thyroid Optimization: Cook goitrogenic vegetables before eating; ensure adequate selenium and iodine.")

    # 5. Check Vitamin D / B12 / Iron Deficiencies
    for lm in (lab_measurements or []):
        t_name = (lm.get("test_name") or lm.get("name") or "").lower()
        status = lm.get("status")
        if "vitamin d" in t_name and status in ["Low", "Critical"]:
            foods_to_eat.update(["Fortified Milk", "Egg Yolks", "Mushrooms", "Sunlight (15 mins morning)"])
            clinical_notes.append("Vitamin D Boost: Pair dietary vitamin D with healthy fats for optimal absorption.")
        elif "hemoglobin" in t_name and status in ["Low", "Critical"]:
            foods_to_eat.update(["Spinach", "Beetroot", "Dates", "Jaggery (Gud)", "Pomegranate", "Amla (Vitamin C)"])
            clinical_notes.append("Iron Synthesis: Pair iron-rich foods with Vitamin C (Lemon/Amla) for enhanced bio-availability.")

    # 6. Apply Allergy Exclusions
    for a in allergies_clean:
        if "peanut" in a or "nut" in a:
            foods_to_avoid.update(["Peanuts", "Tree Nuts", "Peanut Butter"])
            foods_to_eat.difference_update(["Walnuts", "Almonds"])
        if "lactose" in a or "milk" in a or "dairy" in a:
            foods_to_avoid.update(["Milk", "Curd", "Paneer", "Butter", "Cheese"])
            foods_to_eat.difference_update(["Fortified Milk", "Yogurt"])
            foods_to_eat.update(["Soy Milk", "Almond Milk", "Tofu"])
        if "gluten" in a or "wheat" in a:
            foods_to_avoid.update(["Roti (Wheat)", "Bread", "Pasta", "Semolina (Suji)"])
            foods_to_eat.update(["Ragi Roti", "Jowar Roti", "Brown Rice", "Quinoa"])

    # Defaults if lists are small
    if not foods_to_eat:
        foods_to_eat.update(["Green Vegetables", "Fresh Fruits", "Whole Grains", "Lentils & Dal", "Nuts & Seeds"])
    if not foods_to_avoid:
        foods_to_avoid.update(["Ultra-processed Foods", "Sugary Carbonated Drinks", "Deep Fried Foods", "Excessive Alcohol"])

    return {
        "foods_to_eat": sorted(list(foods_to_eat)),
        "foods_to_avoid": sorted(list(foods_to_avoid)),
        "clinical_notes": clinical_notes
    }
