from typing import Dict, Any, List

INDIAN_MEALS = {
    "vegetarian": {
        "breakfast": [
            "Vegetable Poha with peanuts + 1 cup Lemon Green Tea (250 kcal | 6g Protein)",
            "Moong Dal Chilla (2) with mint chutney + Sprouted Moong Salad (280 kcal | 14g Protein)",
            "Oats Upma with veggies + 5 soaked Almonds (260 kcal | 8g Protein)",
            "Besan Chilla with Paneer stuffing + Herbal Tea (300 kcal | 15g Protein)",
            "Idli (2) with Sambhar & Coconut Chutney (240 kcal | 7g Protein)",
            "Vegetable Paratha (1) with Curd (290 kcal | 9g Protein)",
            "Paneer & Vegetable Sandwich in whole wheat bread (310 kcal | 16g Protein)"
        ],
        "snack_morning": [
            "1 Apple or Guava + 4 Walnuts (120 kcal)",
            "1 Bowl Papaya / Pomegranate (90 kcal)",
            "1 Glass Buttermilk (Chaas) with roasted cumin (60 kcal)",
            "Roasted Chana (1 small bowl) (110 kcal)"
        ],
        "lunch": [
            "2 Whole Wheat Roti + 1 Bowl Yellow Dal + Palak Sabzi + Cucumber Salad (380 kcal | 16g Protein)",
            "1 Bowl Brown Rice + Rajma Curry + Mixed Green Salad + Curd (420 kcal | 18g Protein)",
            "2 Multigrain Roti + Paneer Bhurji + Tomato Salad (410 kcal | 22g Protein)",
            "1 Bowl Vegetable Khichdi + Kadhi + Roasted Papad (350 kcal | 12g Protein)",
            "2 Jowar Roti + Chole Curry + Cabbage Sambharo (390 kcal | 15g Protein)",
            "2 Ragi Roti + Mix Veg Sabzi + Sprouted Salad + Curd (370 kcal | 14g Protein)",
            "1 Bowl Brown Rice + Lauki Dal + Beetroot Salad (360 kcal | 13g Protein)"
        ],
        "snack_evening": [
            "Green Tea + 1 Handful Roasted Makhana (100 kcal)",
            "1 Glass Coconut Water + 5 Almonds (90 kcal)",
            "Sprouts Bhel with pomegranate & lemon (120 kcal)",
            "Boiled Kala Chana chaat with coriander & cucumber (130 kcal)"
        ],
        "dinner": [
            "1 Bowl Lauki & Spinach Soup + 1 Multigrain Roti + Grilled Paneer (310 kcal | 18g Protein)",
            "1 Bowl Moong Dal Soup + Sauteed Vegetables & Tofu (290 kcal | 17g Protein)",
            "1 Whole Wheat Roti + Baingan Bharta + Yellow Dal (320 kcal | 12g Protein)",
            "Vegetable Oats Khichdi + 1 Bowl Curd (280 kcal | 11g Protein)",
            "1 Bowl Tomato Basil Soup + Grilled Cottage Cheese Salad (300 kcal | 19g Protein)",
            "2 Roti + Bhindi Sabzi + Cucumber Tomato Salad (320 kcal | 10g Protein)",
            "1 Bowl Mix Veg Soup + Stir-fried Tofu & Mushrooms (270 kcal | 16g Protein)"
        ]
    },
    "non_vegetarian": {
        "breakfast": [
            "2 Boiled Eggs / Egg Omelette with veggies + 1 slice Whole Wheat Toast (280 kcal | 18g Protein)",
            "Chicken & Veggie Sandwich in Whole Wheat Toast + Green Tea (320 kcal | 22g Protein)",
            "Egg Scramble with spinach + 5 Almonds (260 kcal | 16g Protein)"
        ],
        "lunch": [
            "2 Roti + Grilled Chicken Breast (150g) + Cucumber Salad (410 kcal | 38g Protein)",
            "1 Bowl Brown Rice + Fish Curry (Rohu/Salmon) + Steamed Broccoli (430 kcal | 32g Protein)",
            "2 Multigrain Roti + Chicken Dal + Green Salad (400 kcal | 34g Protein)"
        ],
        "dinner": [
            "1 Bowl Clear Chicken Soup + Sauteed Veggies & Grilled Fish (290 kcal | 30g Protein)",
            "Egg Curry (2 eggs) + 1 Roti + Mixed Salad (320 kcal | 20g Protein)",
            "Stir-fried Chicken with Bell Peppers & Zucchini (280 kcal | 35g Protein)"
        ]
    }
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def generate_7day_meal_plan(diet_preference: str = "vegetarian", target_calories: int = 1600) -> List[Dict[str, Any]]:
    pref = "non_vegetarian" if "non" in (diet_preference or "").lower() or "chicken" in (diet_preference or "").lower() else "vegetarian"
    meals_db = INDIAN_MEALS.get(pref, INDIAN_MEALS["vegetarian"])

    plan = []
    for i, day in enumerate(DAYS):
        bf = meals_db["breakfast"][i % len(meals_db["breakfast"])]
        sn1 = meals_db["snack_morning"][i % len(meals_db["snack_morning"])]
        ln = meals_db["lunch"][i % len(meals_db["lunch"])]
        sn2 = meals_db["snack_evening"][i % len(meals_db["snack_evening"])]
        dn = meals_db["dinner"][i % len(meals_db["dinner"])]

        plan.append({
            "day": day,
            "breakfast": bf,
            "mid_morning_snack": sn1,
            "lunch": ln,
            "evening_snack": sn2,
            "dinner": dn,
            "estimated_calories": target_calories,
            "hydration_target": "2.8 - 3.2 Liters"
        })

    return plan
