import datetime
from sqlalchemy.orm import Session
from models import User, MedicalDocument, HealthProfile
from services.trend_analysis_service import get_tracked_trends

def build_pdf_context(db: Session, doc_id: int) -> dict:
    doc = db.query(MedicalDocument).filter(MedicalDocument.id == doc_id).first()
    if not doc:
        raise ValueError(f"Document {doc_id} not found")

    user = db.query(User).filter(User.id == doc.user_id).first()
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == doc.user_id).first()

    user_name = user.name if user else "Patient"
    age = profile.age if profile and profile.age else "N/A"
    gender = profile.gender if profile and profile.gender else "N/A"
    conditions = profile.conditions if profile and profile.conditions else []
    allergies = profile.allergies if profile and profile.allergies else []

    conditions_str = ", ".join(conditions) if conditions else "None reported"
    allergies_str = ", ".join(allergies) if allergies else "No known allergies"

    structured = doc.structured_data or {}
    lab_results = []
    
    # Process lab values from structured_data
    labs_raw = structured.get("lab_values", [])
    for l in labs_raw:
        if isinstance(l, dict):
            status = l.get("status", "Normal")
            lab_results.append({
                "name": l.get("name") or l.get("test_name", "Lab Marker"),
                "value": l.get("value", "-"),
                "unit": l.get("unit", ""),
                "reference": l.get("reference_range") or l.get("reference", "Standard"),
                "status": status
            })

    # Process medicines from structured_data
    medicines = []
    meds_raw = structured.get("medicines", [])
    for m in meds_raw:
        if isinstance(m, dict):
            medicines.append({
                "name": m.get("name") or m.get("medicine_name", "Medication"),
                "dosage": m.get("dosage", ""),
                "frequency": m.get("frequency", ""),
                "duration": m.get("duration", ""),
                "instructions": m.get("instructions", "As prescribed")
            })

    # Fetch comparative lab trends
    lab_trends = get_tracked_trends(db, doc.user_id)

    # Collect warnings & recommendations
    warnings = doc.abnormal_values or []
    recommendations = []
    if doc.ai_summary:
        if "borderline" in doc.ai_summary.lower() or "elevated" in doc.ai_summary.lower():
            recommendations.append("Follow up with your primary physician to recheck elevated markers.")
        if allergies and medicines:
            recommendations.append(f"Ensure your doctor is aware of your allergies ({allergies_str}) when starting new prescriptions.")
    if not recommendations:
        recommendations.append("Maintain a balanced hydration and lifestyle schedule as recorded in your Health Profile.")

    return {
        "document_id": doc.id,
        "generated_date": datetime.datetime.utcnow().strftime("%B %d, %Y - %H:%M UTC"),
        "user_name": user_name,
        "age": age,
        "gender": gender,
        "conditions_str": conditions_str,
        "allergies_str": allergies_str,
        "file_name": doc.file_name,
        "document_type": (doc.document_type or "Medical Document").replace("_", " ").title(),
        "upload_date": doc.created_at.strftime("%Y-%m-%d %H:%M") if doc.created_at else "Today",
        "ai_summary": doc.ai_summary or "No summary generated for this document.",
        "lab_results": lab_results,
        "medicines": medicines,
        "lab_trends": lab_trends,
        "warnings": warnings,
        "recommendations": recommendations
    }
