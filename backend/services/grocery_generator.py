from typing import Dict, List

def generate_weekly_grocery_list(diet_preference: str = "vegetarian") -> Dict[str, List[str]]:
    """
    Generates a categorized 9-group weekly grocery shopping list.
    Categories:
    1. Vegetables
    2. Fruits
    3. Whole Grains
    4. Lentils
    5. Dairy
    6. Protein Sources
    7. Nuts & Seeds
    8. Healthy Oils
    9. Spices
    """
    pref = (diet_preference or "").lower()
    is_non_veg = any(k in pref for k in ["non", "chicken", "egg", "fish", "meat"])

    grocery_list = {
        "Vegetables": [
            "Spinach & Palak (2 bunches)",
            "Cucumber & Tomatoes (1.5 kg each)",
            "Lauki (Bottle Gourd) & Ridge Gourd (2 pcs)",
            "Bitter Gourd (Karela) & Methi (1 bunch)",
            "Bell Peppers, Carrots & Beetroot (1 kg total)",
            "Onions & Garlic (1.5 kg total)",
            "Cabbage & Broccoli (1 head each)"
        ],
        "Fruits": [
            "Apples & Papaya (1 kg each)",
            "Pomegranates & Guava (500g total)",
            "Lemons (6 pcs)",
            "Oranges & Pears (1 kg)"
        ],
        "Whole Grains": [
            "Rolled Oats (1 kg)",
            "Multigrain Atta / Whole Wheat Atta (5 kg)",
            "Brown Rice / Red Rice (2 kg)",
            "Ragi & Jowar Flour (1 kg)",
            "Quinoa (500g)"
        ],
        "Lentils": [
            "Yellow Moong Dal (1 kg)",
            "Rajma (Kidney Beans) & Chole (500g each)",
            "Green Moong & Kala Chana for Sprouts (500g each)",
            "Toor Dal & Chana Dal (1 kg total)"
        ],
        "Dairy": [
            "Low-fat Curd / Dahi (1.5 kg)",
            "Double Toned Milk / Soy Milk (2 Liters)",
            "Buttermilk / Chaas (1 Liter)"
        ],
        "Protein Sources": [
            "Fresh Paneer (500g)" if not is_non_veg else "Fresh Paneer & Tofu (500g)",
            "Tofu (Organic Soy) (500g)",
            "Sprouted Moong & Chana (500g)"
        ],
        "Nuts & Seeds": [
            "Raw Almonds & Walnuts (250g each)",
            "Flaxseeds & Chia Seeds (200g each)",
            "Roasted Makhana & Roasted Chana (500g total)",
            "Pumpkin & Sunflower Seeds (150g)"
        ],
        "Healthy Oils": [
            "Extra Virgin Olive Oil (500 ml)",
            "Cold Pressed Mustard Oil / Sesame Oil (1 Liter)",
            "Pure Desi Ghee (250 ml - for moderate use)"
        ],
        "Spices": [
            "Turmeric Powder (Haldi)",
            "Cumin Seeds & Roasted Cumin Powder (Jeera)",
            "Cinnamon Sticks & Powder (Dalchini)",
            "Pink Himalayan Salt / Low-Sodium Salt",
            "Black Pepper & Fenugreek Seeds (Methi Dana)"
        ]
    }

    if is_non_veg:
        grocery_list["Protein Sources"].extend([
            "Eggs (1-2 Dozen)",
            "Skinless Chicken Breast (1 kg)",
            "Fresh Fish / Salmon / Rohu (500g)"
        ])

    # Deduplicate each list category
    deduped_list = {}
    for cat, items in grocery_list.items():
        seen = set()
        cleaned = []
        for item in items:
            if item not in seen:
                seen.add(item)
                cleaned.append(item)
        deduped_list[cat] = cleaned

    return deduped_list
