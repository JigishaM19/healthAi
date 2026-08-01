import bcrypt
import datetime
import re
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import (
    User, UserSettings, HealthProfile, Conversation, Message, 
    TimelineEvent, MedicalDocument, Medication, LabMeasurement, 
    HealthMemory, NotificationLog, TrustedDevice, UserSession, ConnectedDevice
)
from services.timeline_service import create_event

def get_or_create_user_settings(db: Session, user_id: int) -> UserSettings:
    st = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if not st:
        st = UserSettings(user_id=user_id)
        db.add(st)
        db.commit()
        db.refresh(st)
    return st

def update_account_info(db: Session, user_id: int, name: str, email: str, phone_number: str = None) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    clean_email = email.lower().strip()
    if clean_email != user.email:
        existing = db.query(User).filter(User.email == clean_email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email address is already registered to another account")
        user.email = clean_email

    if phone_number:
        clean_phone = phone_number.strip()
        if not re.match(r"^\+?[0-9\s\-]{7,15}$", clean_phone):
            raise HTTPException(status_code=400, detail="Invalid phone number format. Please provide a valid 7 to 15 digit phone number.")
        user.phone_number = clean_phone
    else:
        user.phone_number = None

    user.name = name.strip()

    st = get_or_create_user_settings(db, user_id)
    st.phone_number = user.phone_number
    db.commit()
    db.refresh(user)

    # Log Timeline Event
    try:
        create_event(
            db=db,
            user_id=user_id,
            event_type="profile",
            title="Account Profile Updated",
            summary=f"User profile updated: Name '{user.name}', Email '{user.email}'.",
            details={"name": user.name, "email": user.email, "phone_number": user.phone_number}
        )
    except Exception as te:
        print("[SettingsService] Timeline event skip:", te)

    return user

def validate_password_strength(password: str):
    """Enforces strict password strength policy."""
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not any(c.isupper() for c in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character (!@#$%^&*)")

def update_password_info(db: Session, user_id: int, current_pass: str, new_pass: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(current_pass.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect current password. Please try again.")

    if current_pass == new_pass:
        raise HTTPException(status_code=400, detail="New password cannot be identical to your current password.")

    validate_password_strength(new_pass)

    hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password_hash = hashed
    db.commit()

    # Log Timeline Event
    try:
        create_event(
            db=db,
            user_id=user_id,
            event_type="profile",
            title="Password Security Updated",
            summary="User successfully changed account password.",
            details={"updated_at": datetime.datetime.utcnow().isoformat()}
        )
    except Exception as te:
        print("[SettingsService] Timeline event skip:", te)

    return {"message": "Password updated successfully"}

def toggle_2fa_settings(db: Session, user_id: int, enabled: int, preferred_method: str = "email"):
    st = get_or_create_user_settings(db, user_id)
    st.two_factor_enabled = 1 if enabled else 0
    st.preferred_2fa_method = preferred_method
    db.commit()
    return {
        "message": f"Two-Factor Authentication (2FA) {'enabled' if enabled else 'disabled'} successfully",
        "two_factor_enabled": st.two_factor_enabled,
        "preferred_2fa_method": st.preferred_2fa_method
    }

def get_user_active_sessions(db: Session, user_id: int) -> List[Dict[str, Any]]:
    sessions = db.query(UserSession).filter(UserSession.user_id == user_id).order_by(UserSession.last_active.desc()).all()
    if not sessions:
        # Fallback to trusted devices or current session
        user = db.query(User).filter(User.id == user_id).first()
        return [{
            "id": 1,
            "device": user.last_login_device or "Chrome Browser (Current)",
            "browser": "Chrome 122.0",
            "os": "Windows 11 / Desktop",
            "ip": user.last_login_ip or "127.0.0.1",
            "location": "Local Session",
            "is_current": True,
            "last_active": user.last_login_at.isoformat() if user and user.last_login_at else datetime.datetime.utcnow().isoformat()
        }]

    return [{
        "id": s.id,
        "device": s.device or "Web Browser",
        "browser": s.browser or "Chrome",
        "os": s.os or "Desktop",
        "ip": s.ip or "127.0.0.1",
        "location": s.location or "Unknown",
        "is_current": bool(s.is_current),
        "last_active": s.last_active.isoformat() if s.last_active else datetime.datetime.utcnow().isoformat()
    } for s in sessions]

def logout_other_sessions(db: Session, user_id: int):
    db.query(UserSession).filter(UserSession.user_id == user_id, UserSession.is_current == 0).delete()
    db.commit()
    return {"message": "Successfully logged out from all other active sessions and devices."}

def get_connected_wearables(db: Session, user_id: int) -> List[Dict[str, Any]]:
    devices = db.query(ConnectedDevice).filter(ConnectedDevice.user_id == user_id).all()
    default_providers = ["google_fit", "apple_health", "fitbit", "samsung_health"]
    
    connected_map = {d.provider: d for d in devices}
    result = []
    
    for prov in default_providers:
        d = connected_map.get(prov)
        result.append({
            "provider": prov,
            "name": prov.replace("_", " ").title(),
            "connected": bool(d.connected) if d else False,
            "account_id": d.account_id if d else None,
            "last_sync": d.last_sync.isoformat() if d and d.last_sync else None
        })

    return result

def toggle_wearable_connection(db: Session, user_id: int, provider: str, connect: bool, account_id: str = None):
    prov_clean = provider.lower().strip()
    device = db.query(ConnectedDevice).filter(
        ConnectedDevice.user_id == user_id,
        ConnectedDevice.provider == prov_clean
    ).first()

    if not device:
        device = ConnectedDevice(
            user_id=user_id,
            provider=prov_clean,
            account_id=account_id or f"{user_id}_{prov_clean}_acc",
            connected=1 if connect else 0,
            last_sync=datetime.datetime.utcnow()
        )
        db.add(device)
    else:
        device.connected = 1 if connect else 0
        device.last_sync = datetime.datetime.utcnow()
        if account_id:
            device.account_id = account_id

    db.commit()
    return {
        "message": f"Successfully {'connected' if connect else 'disconnected'} {prov_clean.replace('_', ' ').title()}",
        "provider": prov_clean,
        "connected": bool(device.connected)
    }

def export_user_health_data(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    st = get_or_create_user_settings(db, user_id)
    events = db.query(TimelineEvent).filter(TimelineEvent.user_id == user_id).all()
    docs = db.query(MedicalDocument).filter(MedicalDocument.user_id == user_id).all()
    meds = db.query(Medication).filter(Medication.user_id == user_id).all()
    labs = db.query(LabMeasurement).filter(LabMeasurement.user_id == user_id).all()
    memories = db.query(HealthMemory).filter(HealthMemory.user_id == user_id).all()
    notifications = db.query(NotificationLog).filter(NotificationLog.user_id == user_id).all()

    return {
        "export_metadata": {
            "application": "HealthAI Platform",
            "version": "1.0.0",
            "export_date": datetime.datetime.utcnow().isoformat(),
            "format": "JSON Health Record Archive"
        },
        "user_account": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "created_at": user.created_at.isoformat() if user.created_at else None
        },
        "user_settings": {
            "theme": st.theme,
            "language": st.language,
            "units": st.units,
            "date_format": st.date_format,
            "time_format": st.time_format,
            "notifications": {
                "medication_reminders": bool(st.medication_reminders),
                "hydration_reminders": bool(st.hydration_reminders),
                "exercise_reminders": bool(st.exercise_reminders),
                "sleep_reminders": bool(st.sleep_reminders),
                "appointment_reminders": bool(st.appointment_reminders),
                "report_notifications": bool(st.report_notifications)
            },
            "security": {
                "two_factor_enabled": bool(st.two_factor_enabled),
                "preferred_2fa_method": st.preferred_2fa_method,
                "research_sharing": bool(st.anonymized_research_sharing)
            }
        },
        "health_profile": {
            "age": profile.age if profile else None,
            "gender": profile.gender if profile else None,
            "height_cm": profile.height_cm if profile else None,
            "weight_kg": profile.weight_kg if profile else None,
            "conditions": profile.conditions if profile else [],
            "allergies": profile.allergies if profile else [],
            "medications": profile.medications if profile else [],
            "goals": profile.goals if profile else [],
            "blood_group": profile.blood_group if profile else None,
            "emergency_contact": profile.emergency_contact if profile else None
        },
        "summary_counts": {
            "timeline_events_count": len(events),
            "medical_documents_count": len(docs),
            "medications_count": len(meds),
            "lab_measurements_count": len(labs),
            "health_memories_count": len(memories),
            "notification_logs_count": len(notifications)
        },
        "medications": [{"name": m.medicine_name, "dosage": m.dosage, "frequency": m.frequency, "active": m.active} for m in meds],
        "lab_measurements": [{"test": l.test_name, "value": l.value, "unit": l.unit, "status": l.status, "date": l.test_date.isoformat() if l.test_date else None} for l in labs],
        "timeline_events": [{"type": e.event_type, "title": e.title, "summary": e.summary, "date": e.timestamp.isoformat() if e.timestamp else None} for e in events[:20]],
        "health_memories": [{"type": m.memory_type, "title": m.title, "summary": m.summary, "date": m.created_at.isoformat() if m.created_at else None} for m in memories[:20]]
    }

def delete_user_account(db: Session, user_id: int, password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect password. Account deletion aborted for security.")

    # Delete User (SQLAlchemy cascading relationship deletes profile, conversations, messages, events, docs, settings)
    db.delete(user)
    db.commit()
    return {"message": "Account and all associated personal health records deleted permanently."}
