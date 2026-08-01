from sqlalchemy.orm import Session
from typing import Dict, Any, List
from models import Medication
from services.notification_service import dispatch_notification

async def send_medication_reminder(db: Session, user_id: int, medication_name: str) -> Dict[str, Any]:
    await dispatch_notification(db, user_id, "medication_reminder", {"medication_name": medication_name})
    return {"message": f"Medication reminder sent for {medication_name}"}

async def send_appointment_reminder(db: Session, user_id: int, doctor_name: str, appointment_time: str) -> Dict[str, Any]:
    await dispatch_notification(db, user_id, "appointment_reminder", {
        "doctor_name": doctor_name,
        "appointment_time": appointment_time
    })
    return {"message": f"Appointment reminder sent for {doctor_name} at {appointment_time}"}

def get_active_reminders(db: Session, user_id: int) -> List[Dict[str, Any]]:
    meds = db.query(Medication).filter(Medication.user_id == user_id, Medication.active == "active").all()
    reminders = []
    for m in meds:
        reminders.append({
            "id": m.id,
            "type": "medication",
            "title": f"Take {m.medicine_name}",
            "dosage": m.dosage or "5mg",
            "frequency": m.frequency or "Daily",
            "doctor": m.prescribing_doctor or "Primary Care"
        })
    return reminders
