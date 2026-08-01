import bcrypt
import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User, UserSettings, HealthProfile, Conversation, Message, TimelineEvent, MedicalDocument, Medication, LabMeasurement, HealthMemory

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

    if email != user.email:
        existing = db.query(User).filter(User.email == email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email address is already in use")
        user.email = email

    user.name = name
    
    st = get_or_create_user_settings(db, user_id)
    st.phone_number = phone_number
    db.commit()
    db.refresh(user)
    return user

def update_password_info(db: Session, user_id: int, current_pass: str, new_pass: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(current_pass.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password_hash = hashed
    db.commit()
    return {"message": "Password updated successfully"}

def export_user_health_data(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    events = db.query(TimelineEvent).filter(TimelineEvent.user_id == user_id).all()
    docs = db.query(MedicalDocument).filter(MedicalDocument.user_id == user_id).all()
    meds = db.query(Medication).filter(Medication.user_id == user_id).all()
    labs = db.query(LabMeasurement).filter(LabMeasurement.user_id == user_id).all()
    memories = db.query(HealthMemory).filter(HealthMemory.user_id == user_id).all()

    return {
        "export_date": datetime.datetime.utcnow().isoformat(),
        "user": {
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None
        },
        "health_profile": {
            "age": profile.age if profile else None,
            "gender": profile.gender if profile else None,
            "height_cm": profile.height_cm if profile else None,
            "weight_kg": profile.weight_kg if profile else None,
            "conditions": profile.conditions if profile else [],
            "allergies": profile.allergies if profile else [],
            "medications": profile.medications if profile else []
        },
        "timeline_events_count": len(events),
        "medical_documents_count": len(docs),
        "medications_count": len(meds),
        "lab_measurements_count": len(labs),
        "health_memories_count": len(memories),
        "medications": [{"name": m.medicine_name, "dosage": m.dosage, "frequency": m.frequency} for m in meds],
        "lab_measurements": [{"test": l.test_name, "value": l.value, "unit": l.unit, "date": l.test_date.isoformat() if l.test_date else None} for l in labs]
    }

def delete_user_account(db: Session, user_id: int, password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect password. Account deletion aborted.")

    db.delete(user)
    db.commit()
    return {"message": "Account and all associated health records deleted successfully"}
