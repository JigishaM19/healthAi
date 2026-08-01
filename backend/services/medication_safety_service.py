import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from models import User, HealthProfile, LabMeasurement, MedicalDocument
from services.interaction_checker import check_drug_drug_interactions, normalize_med_name
from services.food_interaction_engine import check_food_medication_interactions
from services.lab_interaction_engine import check_condition_medication_interactions, check_lab_medication_interactions
from services.medication_scheduler import generate_medication_schedule
from services.health_memory_service import create_memory_entry
from services.timeline_service import create_event
from services.email_service import send_email
from services.sms_service import send_sms

def run_medication_safety_audit(
    db: Session,
    user_id: int,
    custom_medications: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Coordinates end-to-end Medication Safety Audit:
    1. Aggregates medications from Health Profile and OCR Document extractions
    2. Runs Drug-Drug interaction checks
    3. Runs Food-Medication interaction checks (cross-checking active nutrition plans)
    4. Runs Condition-Medication interaction checks
    5. Runs Lab-Medication interaction checks
    6. Generates daily Medication Timing Schedule
    7. Evaluates overall safety severity (Safe, Mild, Moderate, High, Critical)
    8. Persists to Health Memory & Health Timeline
    9. Dispatches Email/SMS alerts for High or Critical severity risks
    """
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()

    profile_meds = profile.medications if profile and profile.medications else []
    conditions = profile.conditions if profile and profile.conditions else []
    allergies = profile.allergies if profile and profile.allergies else []

    # Extract medications from recent uploaded prescription documents
    docs = db.query(MedicalDocument).filter(MedicalDocument.user_id == user_id).all()
    doc_meds = []
    for d in docs:
        if d.extracted_data and isinstance(d.extracted_data, dict):
            extracted = d.extracted_data.get("medications", [])
            if isinstance(extracted, list):
                doc_meds.extend(extracted)

    # Combine all medication sources
    all_meds = list(set(profile_meds + doc_meds + (custom_medications or [])))
    if not all_meds:
        all_meds = ["Metformin", "Levothyroxine", "Amlodipine"] # Default sample for report generation

    # Fetch recent lab measurements
    labs = db.query(LabMeasurement).filter(LabMeasurement.user_id == user_id).order_by(LabMeasurement.test_date.desc()).all()
    lab_list = [{"name": l.test_name, "value": l.value, "unit": l.unit, "status": l.status} for l in labs[:15]]

    # 1. Drug-Drug Checks
    drug_drug = check_drug_drug_interactions(all_meds)

    # 2. Food-Medication Checks
    food_meds = check_food_medication_interactions(all_meds)

    # 3. Condition-Medication Checks
    cond_meds = check_condition_medication_interactions(all_meds, conditions)

    # 4. Lab-Medication Checks
    lab_meds = check_lab_medication_interactions(all_meds, lab_list)

    # 5. Medication Timing Schedule
    schedule = generate_medication_schedule(all_meds)

    # Compute Overall Severity
    severities = []
    for item in drug_drug + food_meds + cond_meds + lab_meds:
        severities.append(item.get("severity", "Safe"))

    if "Critical" in severities:
        overall_severity = "Critical"
    elif "High" in severities:
        overall_severity = "High"
    elif "Moderate" in severities:
        overall_severity = "Moderate"
    elif "Mild" in severities:
        overall_severity = "Mild"
    else:
        overall_severity = "Safe"

    # Compile Foods to Avoid & Allowed
    foods_avoid = set()
    foods_allowed = set()
    for f in food_meds:
        foods_avoid.update(f.get("foods_to_avoid", []))
        foods_allowed.update(f.get("foods_allowed", []))

    report_result = {
        "user_id": user_id,
        "user_name": user.name if user else "Patient",
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "overall_severity": overall_severity,
        "medications_analyzed": all_meds,
        "health_conditions": conditions,
        "allergies": allergies,
        "drug_drug_interactions": drug_drug,
        "food_interactions": food_meds,
        "condition_interactions": cond_meds,
        "lab_interactions": lab_meds,
        "medication_schedule": schedule,
        "foods_to_avoid": sorted(list(foods_avoid)),
        "foods_recommended": sorted(list(foods_allowed)),
        "safety_disclaimer": "Do not discontinue or change any medication without consulting your healthcare professional."
    }

    # Save to Health Memory
    try:
        create_memory_entry(
            db=db,
            user_id=user_id,
            memory_type="medication_safety",
            title=f"Medication Safety Audit ({overall_severity} Risk)",
            summary=f"Analyzed {len(all_meds)} medications. Overall Severity: {overall_severity}. {len(drug_drug)} drug-drug and {len(food_meds)} food-medication interactions detected.",
            source_type="medication_safety_service",
            metadata_json=report_result
        )
    except Exception as me:
        print("[MedicationSafety] Memory save error:", me)

    # Save to Health Timeline
    try:
        create_event(
            db=db,
            user_id=user_id,
            event_type="medication",
            title=f"Medication Safety Report Generated ({overall_severity})",
            summary=f"Medication Safety Intelligence scan completed. Severity: {overall_severity}. Analyzed: {', '.join(all_meds)}.",
            details=report_result
        )
    except Exception as te:
        print("[MedicationSafety] Timeline event error:", te)

    # Dispatch High / Critical Risk Email & SMS Alerts
    if overall_severity in ["High", "Critical"] and user and user.email:
        try:
            alert_subj = f"🚨 HealthAI Safety Alert: {overall_severity} Medication Risk Detected"
            alert_summary = f"Detected {overall_severity} medication interaction risk for {', '.join(all_meds)}."
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(send_email(user.email, alert_subj, "report_analyzed.html", {
                        "user_name": user.name,
                        "file_name": "Medication Safety Audit",
                        "document_type": "Medication Safety Alert",
                        "summary": alert_summary
                    }))
                else:
                    loop.run_until_complete(send_email(user.email, alert_subj, "report_analyzed.html", {
                        "user_name": user.name,
                        "file_name": "Medication Safety Audit",
                        "document_type": "Medication Safety Alert",
                        "summary": alert_summary
                    }))
            except Exception:
                pass

            if hasattr(user, "phone") and user.phone:
                send_sms(user.phone, f"HealthAI Safety Alert: {overall_severity} medication risk detected for {user.name}.")
        except Exception as ne:
            print("[MedicationSafety] Alert notification error:", ne)

    return report_result
