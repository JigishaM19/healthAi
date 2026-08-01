from typing import Dict, List

def generate_weekly_grocery_list(diet_preference: str = "vegetarian") -> Dict[str, List[str]]:
    pref = (diet_preference or "").lower()
    
    base_list = {
        "Vegetables": [
            "Spinach & Palak (2 bunches)",
            "Cucumber & Tomato (1 kg each)",
            "Lauki (Bottle Gourd) & Ridge Gourd (2 pcs)",
            "Bitter Gourd (Karela) & Methi (1 bunch)",
            "Bell Peppers, Carrots, Beetroot (500g each)"
        ],
        "Fruits": [
            "Apples & Papaya (1 kg)",
            "Pomegranates & Guava (500g)",
            "Lemons (6 pcs)"
        ],
        "Whole Grains & Flour": [
            "Rolled Oats (1 kg)",
            "Multigrain Atta / Whole Wheat Atta (5 kg)",
            "Brown Rice / Red Rice (2 kg)",
            "Ragi & Jowar Flour (1 kg)"
        ],
        "Lentils & Pulses": [
            "Yellow Moong Dal (1 kg)",
            "Rajma (Kidney Beans) & Chole (500g)",
            "Green Moong & Kala Chana for Sprouts (500g)"
        ],
        "Dairy & Dairy Alternatives": [
            "Low-fat Curd / Dahi (1.5 kg)",
            "Fresh Paneer / Tofu (500g)",
            "Double Toned Milk / Almond Milk (2 Liters)"
        ],
        "Nuts & Seeds": [
            "Raw Almonds & Walnuts (250g)",
            "Flaxseeds & Chia Seeds (200g)",
            "Roasted Makhana & Chana (500g)"
        ],
        "Healthy Oils & Spices": [
            "Extra Virgin Olive Oil / Cold Pressed Mustard Oil",
            "Turmeric, Cumin, Roasted Cumin Powder, Cinnamon",
            "Pink Himalayan Salt / Low-Sodium Salt"
        ]
    }

    if "non" in pref or "chicken" in pref or "egg" in pref:
        base_list["Protein & Meat"] = [
            "Eggs (1-2 Dozen)",
            "Skinless Chicken Breast (1 kg)",
            "Fresh Fish / Salmon Fillets (500g)"
        ]

    return base_list
