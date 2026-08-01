from typing import Dict, Any

def classify_document(text: str, filename: str) -> Dict[str, Any]:
    text_lower = (text + " " + filename).lower()

    # Rule-based fast classification keyword matrices
    if any(kw in text_lower for kw in ["cbc", "blood test", "hemoglobin", "cholesterol", "lipid", "thyroid", "tsh", "kidney", "creatinine", "liver", "sgot", "glucose", "pathology", "urinalysis"]):
        return {"document_type": "lab_report", "confidence": 0.95}

    if any(kw in text_lower for kw in ["prescription", "rx", "tab.", "cap.", "syrup", "dosage", "take once daily", "take twice daily", "pharmacy", "refill"]):
        return {"document_type": "prescription", "confidence": 0.94}

    if any(kw in text_lower for kw in ["mg", "strip", "tablet", "capsule", "medicine photo", "tablet packaging"]):
        return {"document_type": "medicine_photo", "confidence": 0.89}

    if any(kw in text_lower for kw in ["discharge", "summary", "admission date", "discharge date", "hospital stay", "inpatient", "ipd"]):
        return {"document_type": "discharge_summary", "confidence": 0.96}

    if any(kw in text_lower for kw in ["x-ray", "mri", "ct scan", "ultrasound", "ecg", "echo", "pet scan", "radiology", "impression:"]):
        return {"document_type": "imaging_report", "confidence": 0.93}

    if any(kw in text_lower for kw in ["vaccine", "vaccination", "immunization", "covid-19 certificate", "booster"]):
        return {"document_type": "vaccination_record", "confidence": 0.97}

    if any(kw in text_lower for kw in ["insurance", "policy", "claim", "reimbursement", "premium", "coverage"]):
        return {"document_type": "insurance_document", "confidence": 0.92}

    if any(kw in text_lower for kw in ["medical certificate", "sick leave", "fitness certificate"]):
        return {"document_type": "medical_certificate", "confidence": 0.91}

    if any(kw in text_lower for kw in ["invoice", "hospital bill", "payment receipt", "charge breakdown"]):
        return {"document_type": "hospital_bill", "confidence": 0.90}

    if any(kw in text_lower for kw in ["referral", "referred to", "consultation note"]):
        return {"document_type": "referral_letter", "confidence": 0.88}

    return {"document_type": "general_medical", "confidence": 0.82}
