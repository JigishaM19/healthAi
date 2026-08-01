from typing import Dict, Any, List

# Comprehensive Medication & Interaction Knowledge Base
# Normalizes generic & brand names, drug-drug, food-drug, condition-drug, lab-drug, and timing rules.

MEDICATION_ALIASES = {
    # Generic & Popular Brands
    "warfarin": "warfarin", "coumadin": "warfarin", "jantoven": "warfarin",
    "aspirin": "aspirin", "ecosprin": "aspirin", "disprin": "aspirin", "bayer": "aspirin",
    "ibuprofen": "ibuprofen", "advil": "ibuprofen", "motrin": "ibuprofen", "brufen": "ibuprofen",
    "naproxen": "naproxen", "aleve": "naproxen", "naprosyn": "naproxen",
    "acetaminophen": "paracetamol", "paracetamol": "paracetamol", "tylenol": "paracetamol", "crocin": "paracetamol", "dolo": "paracetamol", "calpol": "paracetamol",
    "metformin": "metformin", "glucophage": "metformin", "glycomet": "metformin",
    "levothyroxine": "levothyroxine", "synthroid": "levothyroxine", "eltroxin": "levothyroxine", "thyronorm": "levothyroxine",
    "amlodipine": "amlodipine", "norvasc": "amlodipine", "amlogard": "amlodipine",
    "atorvastatin": "atorvastatin", "lipitor": "atorvastatin", "atorva": "atorvastatin",
    "simvastatin": "simvastatin", "zocor": "simvastatin", "simvotin": "simvastatin",
    "rosuvastatin": "rosuvastatin", "crestor": "rosuvastatin", "rosuvas": "rosuvastatin",
    "lisinopril": "lisinopril", "zestril": "lisinopril", "prinivil": "lisinopril",
    "enalapril": "enalapril", "vasotec": "enalapril",
    "losartan": "losartan", "cozaar": "losartan", "repace": "losartan",
    "furosemide": "furosemide", "lasix": "furosemide",
    "hydrochlorothiazide": "hydrochlorothiazide", "hctz": "hydrochlorothiazide", "microzide": "hydrochlorothiazide",
    "spironolactone": "spironolactone", "aldactone": "spironolactone",
    "iron": "iron", "ferrous sulfate": "iron", "ferrous fumarate": "iron", "autrin": "iron", "dexorange": "iron",
    "calcium": "calcium", "calcium carbonate": "calcium", "shelcal": "calcium", "cipcal": "calcium",
    "vitamin d": "vitamin_d", "cholecalciferol": "vitamin_d", "calcirol": "vitamin_d",
    "potassium": "potassium", "k-clor": "potassium", "potklor": "potassium",
    "tetracycline": "tetracycline", "doxycycline": "doxycycline", "dox-sl": "doxycycline",
    "prednisone": "prednisone", "prednisolone": "prednisolone", "wysolone": "prednisolone",
    "atenolol": "atenolol", "tenormin": "atenolol", "metoprolol": "metoprolol", "betaloc": "metoprolol", "propranolol": "propranolol", "inderal": "propranolol"
}

DRUG_DRUG_INTERACTIONS = [
    {
        "drugs": ["warfarin", "aspirin"],
        "severity": "High",
        "category": "Bleeding Risk",
        "description": "Combining Warfarin (anticoagulant) and Aspirin (antiplatelet) significantly increases the risk of severe internal gastrointestinal and intracranial bleeding.",
        "what_to_do": "Consult your prescribing physician immediately before combining these. Do not self-medicate with aspirin.",
        "monitoring": ["Unexplained bruising", "Bleeding gums", "Dark or tarry stools", "Frequent nosebleeds"]
    },
    {
        "drugs": ["ibuprofen", "naproxen"],
        "severity": "High",
        "category": "Duplicate NSAID Therapy",
        "description": "Taking multiple Non-Steroidal Anti-Inflammatory Drugs (NSAIDs) simultaneously increases the risk of acute gastric ulceration, stomach bleeding, and renal dysfunction without providing additional pain relief.",
        "what_to_do": "Use only one NSAID at a time. Switch to Paracetamol for mild fever/pain if suitable.",
        "monitoring": ["Upper abdominal pain", "Nausea", "Heartburn", "Black stools"]
    },
    {
        "drugs": ["amlodipine", "simvastatin"],
        "severity": "Moderate",
        "category": "Statin Toxicity Risk",
        "description": "Amlodipine increases blood concentrations of Simvastatin, raising the risk of muscle toxicity (rhabdomyolysis) and liver enzyme elevation.",
        "what_to_do": "Ensure Simvastatin dose does not exceed 20 mg daily when taken concurrently with Amlodipine.",
        "monitoring": ["Unexplained muscle pain", "Muscle tenderness", "Weakness", "Dark urine"]
    },
    {
        "drugs": ["lisinopril", "potassium"],
        "severity": "High",
        "category": "Hyperkalemia Risk",
        "description": "ACE inhibitors (Lisinopril/Enalapril) reduce potassium excretion. Taking concurrent Potassium supplements can cause dangerous hyperkalemia and cardiac arrhythmias.",
        "what_to_do": "Avoid non-prescription potassium supplements and potassium-based salt substitutes.",
        "monitoring": ["Irregular heartbeats", "Palpitations", "Numbness or tingling", "Muscle weakness"]
    },
    {
        "drugs": ["enalapril", "potassium"],
        "severity": "High",
        "category": "Hyperkalemia Risk",
        "description": "ACE inhibitors reduce renal potassium elimination. Potassium supplementation can cause severe hyperkalemia.",
        "what_to_do": "Monitor serum potassium levels regularly; refrain from taking potassium supplements.",
        "monitoring": ["Heart palpitations", "Chest tightness", "Muscle weakness"]
    },
    {
        "drugs": ["spironolactone", "potassium"],
        "severity": "Critical",
        "category": "Severe Hyperkalemia Risk",
        "description": "Spironolactone is a potassium-sparing diuretic. Combining it with potassium supplements can cause life-threatening hyperkalemia.",
        "what_to_do": "Strictly avoid potassium supplements unless under direct nephrologist oversight.",
        "monitoring": ["Cardiac arrhythmias", "Severe fatigue", "Muscle weakness"]
    },
    {
        "drugs": ["metformin", "alcohol"],
        "severity": "Moderate",
        "category": "Lactic Acidosis Risk",
        "description": "Excessive alcohol consumption while on Metformin increases the risk of rare but severe Lactic Acidosis and acute hypoglycemia.",
        "what_to_do": "Avoid heavy or binge drinking while taking Metformin.",
        "monitoring": ["Severe abdominal distress", "Rapid breathing", "Muscle aches", "Extreme fatigue"]
    },
    {
        "drugs": ["iron", "calcium"],
        "severity": "Moderate",
        "category": "Absorption Inhibition",
        "description": "Calcium binds to iron in the gastrointestinal tract, significantly reducing the intestinal absorption of dietary and supplemental iron.",
        "what_to_do": "Separate Iron and Calcium supplements by at least 2 to 4 hours.",
        "monitoring": ["Hemoglobin levels", "Fatigue", "Pale skin"]
    },
    {
        "drugs": ["levothyroxine", "iron"],
        "severity": "Moderate",
        "category": "Thyroid Hormone Inactivation",
        "description": "Iron supplements bind to Levothyroxine in the stomach, preventing thyroid hormone absorption and leading to unmanaged hypothyroidism.",
        "what_to_do": "Take Levothyroxine on an empty stomach in the morning, and wait at least 4 hours before taking Iron supplements.",
        "monitoring": ["TSH levels", "Fatigue", "Weight gain", "Cold sensitivity"]
    },
    {
        "drugs": ["levothyroxine", "calcium"],
        "severity": "Moderate",
        "category": "Absorption Reduction",
        "description": "Calcium carbonate or citrate binds Levothyroxine, markedly decreasing its bioavailability.",
        "what_to_do": "Take Calcium supplements at least 4 hours apart from Levothyroxine.",
        "monitoring": ["Serum TSH levels", "Thyroid symptoms"]
    }
]

DRUG_FOOD_INTERACTIONS = [
    {
        "drug": "levothyroxine",
        "food": "milk",
        "severity": "Moderate",
        "description": "Calcium in milk and dairy products binds to Levothyroxine in the stomach, impairing thyroid hormone absorption.",
        "foods_to_avoid": ["Milk", "Curd / Yogurt", "Cheese", "Fortified Dairy Drinks"],
        "foods_allowed": ["Water", "Black Tea / Coffee (after 30-60 mins)"],
        "timing_advice": "Take Levothyroxine with plain water on an empty stomach 30 to 60 minutes before breakfast or dairy products."
    },
    {
        "drug": "levothyroxine",
        "food": "dairy",
        "severity": "Moderate",
        "description": "Dairy calcium inhibits Levothyroxine bio-availability.",
        "foods_to_avoid": ["Paneer", "Milk", "Curd"],
        "foods_allowed": ["Water", "Fruit"],
        "timing_advice": "Separate dairy intake by at least 3-4 hours after your morning thyroid dose."
    },
    {
        "drug": "warfarin",
        "food": "spinach",
        "severity": "High",
        "description": "Spinach is exceptionally high in Vitamin K. Sudden increases in dietary Vitamin K counteract Warfarin's anticoagulant effect, increasing blood clot risks.",
        "foods_to_avoid": ["Excessive Spinach (Palak)", "Kale", "Broccoli", "Brussels Sprouts", "Green Tea (high intake)"],
        "foods_allowed": ["Root vegetables", "Carrots", "Cucumbers", "Apples", "Grains"],
        "timing_advice": "Maintain a consistent daily Vitamin K intake; avoid sudden large helpings of leafy greens."
    },
    {
        "drug": "atorvastatin",
        "food": "grapefruit",
        "severity": "Moderate",
        "description": "Grapefruit juice inhibits the CYP3A4 enzyme, leading to elevated blood levels of Atorvastatin and increased risk of muscle breakdown (myopathy).",
        "foods_to_avoid": ["Grapefruit", "Grapefruit Juice", "Seville Oranges"],
        "foods_allowed": ["Sweet Oranges", "Apples", "Bananas", "Berries"],
        "timing_advice": "Avoid consuming grapefruit products while taking statin medications."
    },
    {
        "drug": "simvastatin",
        "food": "grapefruit",
        "severity": "High",
        "description": "Grapefruit juice significantly boosts Simvastatin levels, predisposing patients to rhabdomyolysis.",
        "foods_to_avoid": ["Grapefruit", "Grapefruit Juice"],
        "foods_allowed": ["Oranges", "Apples", "Grapes"],
        "timing_advice": "Strictly avoid grapefruit products when taking Simvastatin."
    },
    {
        "drug": "iron",
        "food": "tea",
        "severity": "Moderate",
        "description": "Tannins and polyphenols in tea and coffee bind to non-heme iron, reducing iron absorption by up to 60-70%.",
        "foods_to_avoid": ["Black Tea", "Green Tea", "Coffee", "Espresso"],
        "foods_allowed": ["Lemon Water (Vitamin C boosts iron absorption)", "Amla Juice", "Orange Juice"],
        "timing_advice": "Do not drink tea or coffee within 1 hour before or 2 hours after taking Iron supplements."
    },
    {
        "drug": "doxycycline",
        "food": "dairy",
        "severity": "Moderate",
        "description": "Calcium in dairy forms insoluble chelates with Doxycycline/Tetracycline, drastically reducing antibiotic efficacy.",
        "foods_to_avoid": ["Milk", "Curd", "Paneer", "Calcium-fortified Juices"],
        "foods_allowed": ["Water", "Non-dairy meals"],
        "timing_advice": "Take Doxycycline with a full glass of water 1 hour before or 2 hours after dairy products."
    }
]

DRUG_CONDITION_INTERACTIONS = [
    {
        "drug": "ibuprofen",
        "condition": "hypertension",
        "severity": "High",
        "description": "NSAIDs like Ibuprofen cause renal sodium and water retention, diminishing the effectiveness of anti-hypertensive medications and elevating blood pressure.",
        "what_to_do": "Use Paracetamol for minor pain; avoid chronic NSAID usage if hypertensive.",
        "monitoring": ["Blood pressure readings"]
    },
    {
        "drug": "ibuprofen",
        "condition": "kidney",
        "severity": "High",
        "description": "NSAIDs inhibit renal prostaglandin synthesis, reducing renal blood flow and worsening acute or chronic renal insufficiency.",
        "what_to_do": "Avoid NSAIDs in patients with compromised kidney function.",
        "monitoring": ["Serum Creatinine", "BUN", "Urine Output"]
    },
    {
        "drug": "naproxen",
        "condition": "kidney",
        "severity": "High",
        "description": "Naproxen poses direct nephrotoxicity risk in patients with chronic kidney disease.",
        "what_to_do": "Avoid NSAIDs; consult nephrologist for pain management alternatives.",
        "monitoring": ["Creatinine clearance", "eGFR"]
    },
    {
        "drug": "prednisolone",
        "condition": "diabetes",
        "severity": "High",
        "description": "Systemic corticosteroids induce hepatic gluconeogenesis and peripheral insulin resistance, causing marked blood glucose spikes.",
        "what_to_do": "Monitor blood glucose frequently; physician may adjust insulin/antidiabetic doses during steroid therapy.",
        "monitoring": ["Fasting & Postprandial Blood Glucose", "HbA1c"]
    },
    {
        "drug": "propranolol",
        "condition": "asthma",
        "severity": "Critical",
        "description": "Non-selective beta blockers block Beta-2 receptors in the lungs, triggering severe bronchospasm and acute asthma attacks.",
        "what_to_do": "Avoid non-selective beta blockers in asthmatic patients; use cardioselective agents if necessary.",
        "monitoring": ["Peak Expiratory Flow", "Shortness of Breath", "Wheezing"]
    },
    {
        "drug": "paracetamol",
        "condition": "liver",
        "severity": "High",
        "description": "High-dose Acetaminophen/Paracetamol can cause severe hepatotoxicity in patients with preexisting liver disease or cirrhosis.",
        "what_to_do": "Limit total daily Paracetamol intake to under 2,000 mg/day under medical supervision.",
        "monitoring": ["SGOT / AST", "SGPT / ALT", "Total Bilirubin"]
    }
]

DRUG_LAB_INTERACTIONS = [
    {
        "drug": "furosemide",
        "lab": "potassium",
        "lab_status": "Low",
        "severity": "High",
        "description": "Furosemide (loop diuretic) causes significant renal potassium wasting. Administering it when blood potassium is low can cause severe hypokalemia and fatal cardiac dysrhythmias.",
        "suggested_monitoring": "Recheck serum potassium; consider oral potassium chloride supplementation under medical advice."
    },
    {
        "drug": "lisinopril",
        "lab": "potassium",
        "lab_status": "High",
        "severity": "High",
        "description": "Lisinopril impairs renal potassium excretion. Elevated blood potassium combined with Lisinopril risks severe hyperkalemic cardiac arrest.",
        "suggested_monitoring": "Repeat serum electrolyte panel; reevaluate ACE inhibitor therapy."
    },
    {
        "drug": "metformin",
        "lab": "b12",
        "lab_status": "Low",
        "severity": "Moderate",
        "description": "Long-term Metformin therapy (> 2 years) interferes with ileal Vitamin B12 absorption, compounding preexisting B12 deficiency and peripheral neuropathy.",
        "suggested_monitoring": "Check Vitamin B12 levels annually; initiate B12 supplementation if indicated."
    },
    {
        "drug": "atorvastatin",
        "lab": "sgpt",
        "lab_status": "High",
        "severity": "High",
        "description": "Elevated liver enzymes (SGPT/ALT > 3x upper limit of normal) combined with statin therapy indicates acute hepatic stress or injury.",
        "suggested_monitoring": "Repeat liver function tests (LFT); temporarily withhold statin if transaminases remain significantly elevated."
    },
    {
        "drug": "warfarin",
        "lab": "inr",
        "lab_status": "High",
        "severity": "Critical",
        "description": "An elevated INR (> 3.5-4.0) while taking Warfarin indicates excessive anticoagulation and imminent major bleeding hazard.",
        "suggested_monitoring": "Contact healthcare provider immediately; hold Warfarin doses and administer Vitamin K if advised."
    }
]

MEDICATION_TIMING_RULES = {
    "levothyroxine": {
        "best_time": "6:30 AM",
        "meal_relation": "Empty stomach (30-60 mins before breakfast)",
        "spacing_rule": "Separate from Calcium, Iron, and Antacids by at least 4 hours."
    },
    "metformin": {
        "best_time": "8:00 AM & 8:00 PM",
        "meal_relation": "With or immediately after meals (reduces stomach upset)",
        "spacing_rule": "Avoid heavy alcohol consumption."
    },
    "amlodipine": {
        "best_time": "8:00 PM",
        "meal_relation": "With or without food (at a consistent time daily)",
        "spacing_rule": "Maintain consistent daily schedule."
    },
    "atorvastatin": {
        "best_time": "9:00 PM",
        "meal_relation": "Evening / Bedtime (hepatic cholesterol synthesis peaks at night)",
        "spacing_rule": "Avoid Grapefruit and Grapefruit Juice."
    },
    "simvastatin": {
        "best_time": "9:00 PM",
        "meal_relation": "Bedtime with evening meal",
        "spacing_rule": "Do not consume Grapefruit juice; check for Amlodipine dose limits."
    },
    "iron": {
        "best_time": "11:00 AM",
        "meal_relation": "Between meals or with Vitamin C (Lemon water)",
        "spacing_rule": "Do not take within 2 hours of Tea, Coffee, Dairy, or Calcium."
    },
    "calcium": {
        "best_time": "1:00 PM & 7:00 PM",
        "meal_relation": "With meals (enhances gastric acid dissolution)",
        "spacing_rule": "Keep 4 hours away from Levothyroxine and Iron."
    },
    "aspirin": {
        "best_time": "8:30 AM",
        "meal_relation": "Immediately after meals with full glass of water",
        "spacing_rule": "Do not combine with other NSAIDs or Warfarin without medical advice."
    },
    "warfarin": {
        "best_time": "6:00 PM",
        "meal_relation": "Consistent time every evening",
        "spacing_rule": "Maintain constant dietary Vitamin K (spinach/kale) levels."
    }
}
