from typing import List, Dict, Any

def get_lab_aware_diet_rules(
    conditions: List[str] = None,
    allergies: List[str] = None,
    lab_measurements: List[Dict[str, Any]] = None,
    lab_trends: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Evaluates patient medical conditions, drug/food allergies, and lab results
    (HbA1c, Glucose, LDL, Hemoglobin, Vitamin D, B12, Sodium, Kidney/Liver markers)
    to generate evidence-based dietary recommendations and exclusions.
    """
    foods_to_eat = set()
    foods_to_avoid = set()
    clinical_notes = []

    conditions_clean = [c.lower() for c in (conditions or [])]
    allergies_clean = [a.lower() for a in (allergies or [])]

    # Helper to check lab test status
    def check_lab_status(test_keywords: List[str]) -> Optional[Dict[str, Any]]:
        for lm in (lab_measurements or []):
            t_name = (lm.get("test_name") or lm.get("name") or "").lower()
            if any(k in t_name for k in test_keywords):
                return lm
        return None

    # 1. Diabetes / Prediabetes / High Glucose / HbA1c
    has_diabetes = any(k in c for c in conditions_clean for k in ["diabet", "prediabet", "insulin"])
    glucose_lab = check_lab_status(["glucose", "hba1c", "fbs", "ppbs"])
    has_high_glucose = glucose_lab and glucose_lab.get("status") in ["High", "Critical"]

    if has_diabetes or has_high_glucose:
        foods_to_eat.update([
            "Oats", "Moong Dal", "Bitter Gourd (Karela)", "Fenugreek (Methi)", 
            "Sprouts", "Chia Seeds", "Cinnamon", "Green Leafy Vegetables", "Ragi & Jowar Roti"
        ])
        foods_to_avoid.update([
            "Sugary Drinks", "White Rice", "Bakery Goods", "Fruit Juices", 
            "Refined Flour (Maida)", "Sweets & Desserts", "Deep-fried Snacks", "Sugar Syrup"
        ])
        clinical_notes.append("Glycemic Management: Emphasize low-GI complex carbohydrates (fiber > 30g/day) paired with lean protein to prevent postprandial glucose spikes.")

    # 2. High Cholesterol / High LDL / Triglycerides / Heart Disease
    has_cholesterol = any(k in c for c in conditions_clean for k in ["cholesterol", "lipid", "heart", "coronary"])
    ldl_lab = check_lab_status(["cholesterol", "ldl", "triglyceride", "lipid"])
    has_high_ldl = ldl_lab and ldl_lab.get("status") in ["High", "Critical"]

    if has_cholesterol or has_high_ldl:
        foods_to_eat.update([
            "Rolled Oats", "Flaxseeds", "Walnuts", "Garlic", "Avocado", 
            "Apples", "Legumes", "Extra Virgin Olive Oil", "Psyllium Husk (Isabgol)"
        ])
        foods_to_avoid.update([
            "Butter & Ghee (excess)", "Red Meat", "Full-fat Dairy", "Fried Snacks", 
            "Trans Fats", "Processed Meats", "Palm Oil", "Coconut Milk (excess)"
        ])
        clinical_notes.append("Cardiovascular & Lipid Control: Increase soluble fiber intake (10g+/day) and limit saturated fats to < 7% of total daily energy to lower LDL cholesterol.")

    # 3. Hypertension / High Blood Pressure
    has_htn = any(k in c for c in conditions_clean for k in ["hypertension", "blood pressure", "bp"])
    if has_htn:
        foods_to_eat.update([
            "Bananas", "Spinach", "Beetroot Juice", "Pomegranates", 
            "Unsalted Seeds", "Coconut Water", "Garlic", "Tender Coconut"
        ])
        foods_to_avoid.update([
            "High Sodium Pickles", "Papad", "Processed Soups", "Salty Snacks", 
            "Canned Foods", "Excess Salt", "Soy Sauce", "Ajinomoto (MSG)"
        ])
        clinical_notes.append("DASH Protocol: Restrict sodium intake to < 2,000 mg/day (under 1 teaspoon salt daily) and boost potassium-rich vegetables.")

    # 4. Thyroid (Hypothyroidism / Hyperthyroidism)
    has_hypo = any("hypothyroid" in c or "thyroid" in c for c in conditions_clean)
    if has_hypo:
        foods_to_eat.update([
            "Brazil Nuts (Selenium)", "Eggs", "Yogurt", "Pumpkin Seeds", "Cooked Vegetables", "Iodized Salt"
        ])
        foods_to_avoid.update([
            "Raw Goitrogens (Raw Cabbage, Raw Cauliflower, Raw Broccoli)", "Soy Products (unfermented)", "Excessive Caffeine"
        ])
        clinical_notes.append("Thyroid Optimization: Ensure goitrogenic vegetables are thoroughly cooked before consumption; maintain adequate selenium and zinc intake.")

    # 5. PCOS / Polycystic Ovarian Syndrome
    has_pcos = any("pcos" in c or "polycystic" in c for c in conditions_clean)
    if has_pcos:
        foods_to_eat.update([
            "Spearmint Tea", "Flaxseeds", "Inositol-rich Foods (Beans, Cantaloupe)", "Berries", "Almonds", "Leafy Greens"
        ])
        foods_to_avoid.update([
            "Refined Sugar", "White Bread", "Dairy (if inflammatory)", "Processed Carbohydrates", "High-GI Snacks"
        ])
        clinical_notes.append("PCOS Hormonal Balance: Consume anti-inflammatory omega-3 fats, spearmint tea, and low-glycemic meals to reduce insulin resistance.")

    # 6. Kidney Disease / Renal Dysfunction
    has_kidney = any(k in c for c in conditions_clean for k in ["kidney", "renal", "creatinine"])
    if has_kidney:
        foods_to_eat.update([
            "Cabbage", "Cauliflower", "Apples", "Berries", "Egg Whites", "White Rice (controlled portion)"
        ])
        foods_to_avoid.update([
            "High Sodium Pickles", "High Potassium Foods (Bananas, Potatoes in excess)", "High Phosphorus Dairy", "Red Meat"
        ])
        clinical_notes.append("Renal Nutrition: Restrict protein to ~0.8 g/kg body weight; monitor sodium, potassium, and phosphorus levels under nephrology guidance.")

    # 7. Liver Disease / Fatty Liver / NAFLD
    has_liver = any(k in c for c in conditions_clean for k in ["liver", "fatty liver", "sgot", "sgpt", "cirrhosis"])
    if has_liver:
        foods_to_eat.update([
            "Green Tea", "Grapefruit", "Walnuts", "Cruciferous Vegetables", "Olive Oil", "Garlic"
        ])
        foods_to_avoid.update([
            "Alcohol", "Added Fructose & High Fructose Corn Syrup", "Deep Fried Foods", "Saturated Fat"
        ])
        clinical_notes.append("Hepatic Care: Eliminate alcohol, restrict refined fructose, and increase antioxidant-rich cruciferous vegetables to reduce hepatic steatosis.")

    # 8. Deficiencies from Lab Measurements (Vitamin D, B12, Hemoglobin/Iron)
    vit_d_lab = check_lab_status(["vitamin d", "vit d", "25-oh"])
    if vit_d_lab and vit_d_lab.get("status") in ["Low", "Critical"]:
        foods_to_eat.update(["Fortified Milk / Soy Milk", "Egg Yolks", "Mushrooms", "Sunlight (15-20 mins morning)"])
        clinical_notes.append("Vitamin D Restoration: Pair dietary Vitamin D with healthy fats (nuts/avocado) for enhanced fat-soluble absorption.")

    vit_b12_lab = check_lab_status(["b12", "cobalamin"])
    if vit_b12_lab and vit_b12_lab.get("status") in ["Low", "Critical"]:
        foods_to_eat.update(["Fortified Cereals", "Milk & Curd", "Eggs", "Nutritional Yeast", "Fish"])
        clinical_notes.append("Vitamin B12 Optimization: Incorporate B12-fortified foods or dietary supplements as recommended by your physician.")

    hb_lab = check_lab_status(["hemoglobin", "hb", "iron", "ferritin"])
    if (hb_lab and hb_lab.get("status") in ["Low", "Critical"]) or any("anemia" in c for c in conditions_clean):
        foods_to_eat.update(["Spinach & Palak", "Beetroot", "Dates", "Jaggery (Gud)", "Pomegranate", "Amla (Vitamin C)"])
        foods_to_avoid.update(["Tea/Coffee with Meals (inhibits iron absorption)"])
        clinical_notes.append("Iron Bio-availability: Pair iron-rich foods with Vitamin C (Lemon/Amla/Citrus); avoid drinking tea or coffee within 1 hour of meals.")

    # 9. Apply Allergy Exclusions
    for a in allergies_clean:
        if "peanut" in a or "nut" in a:
            foods_to_avoid.update(["Peanuts", "Tree Nuts", "Peanut Butter", "Almond Milk"])
            foods_to_eat.difference_update(["Walnuts", "Almonds", "Brazil Nuts (Selenium)"])
        if "lactose" in a or "milk" in a or "dairy" in a:
            foods_to_avoid.update(["Milk", "Curd", "Paneer", "Butter", "Cheese", "Ghee"])
            foods_to_eat.difference_update(["Fortified Milk", "Yogurt", "Low-fat Curd / Dahi (1.5 kg)", "Fresh Paneer / Tofu (500g)"])
            foods_to_eat.update(["Soy Milk", "Almond Milk", "Tofu", "Coconut Milk"])
        if "gluten" in a or "wheat" in a:
            foods_to_avoid.update(["Roti (Wheat)", "Bread", "Pasta", "Semolina (Suji)", "Multigrain Atta"])
            foods_to_eat.update(["Ragi Roti", "Jowar Roti", "Brown Rice", "Quinoa", "Moong Dal Chilla"])

    # Fallback default foods if list is sparse
    if not foods_to_eat:
        foods_to_eat.update(["Green Leafy Vegetables", "Fresh Seasonal Fruits", "Whole Grains (Oats/Brown Rice)", "Lentils & Dal", "Nuts & Seeds"])
    if not foods_to_avoid:
        foods_to_avoid.update(["Ultra-processed Foods", "Sugary Carbonated Beverages", "Deep-fried Snacks", "Excess Alcohol"])

    return {
        "foods_to_eat": sorted(list(foods_to_eat)),
        "foods_to_avoid": sorted(list(foods_to_avoid)),
        "clinical_notes": clinical_notes
    }
