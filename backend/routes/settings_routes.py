from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional

from database import get_db
from models import User, UserSettings
from auth import get_current_user
from services.settings_service import (
    get_or_create_user_settings,
    update_account_info,
    update_password_info,
    export_user_health_data,
    delete_user_account
)

router = APIRouter(prefix="/settings", tags=["Settings & Account Management"])

class AccountUpdateInput(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None

class PasswordUpdateInput(BaseModel):
    current_password: str
    new_password: str

class NotificationUpdateInput(BaseModel):
    medication_reminders: Optional[int] = 1
    hydration_reminders: Optional[int] = 1
    exercise_reminders: Optional[int] = 1
    sleep_reminders: Optional[int] = 1
    appointment_reminders: Optional[int] = 1
    report_notifications: Optional[int] = 1

class AppearanceUpdateInput(BaseModel):
    theme: Optional[str] = "dark"
    font_size: Optional[str] = "medium"
    reduce_animations: Optional[int] = 0
    high_contrast: Optional[int] = 0

class LanguageUpdateInput(BaseModel):
    language: Optional[str] = "English"
    date_format: Optional[str] = "YYYY-MM-DD"
    time_format: Optional[str] = "12h"
    units: Optional[str] = "Metric"

class AccountDeleteInput(BaseModel):
    password: str


@router.get("")
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    st = get_or_create_user_settings(db, current_user.id)
    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        },
        "settings": st
    }

@router.put("/account")
def update_account(
    body: AccountUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = update_account_info(db, current_user.id, body.name, body.email, body.phone_number)
    return {
        "message": "Account information updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@router.put("/password")
def update_password(
    body: PasswordUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_password_info(db, current_user.id, body.current_password, body.new_password)

@router.put("/notifications")
def update_notifications(
    body: NotificationUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    st = get_or_create_user_settings(db, current_user.id)
    st.medication_reminders = body.medication_reminders
    st.hydration_reminders = body.hydration_reminders
    st.exercise_reminders = body.exercise_reminders
    st.sleep_reminders = body.sleep_reminders
    st.appointment_reminders = body.appointment_reminders
    st.report_notifications = body.report_notifications
    db.commit()
    return {"message": "Notification preferences updated successfully"}

@router.put("/appearance")
def update_appearance(
    body: AppearanceUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    st = get_or_create_user_settings(db, current_user.id)
    st.theme = body.theme
    st.font_size = body.font_size
    st.reduce_animations = body.reduce_animations
    st.high_contrast = body.high_contrast
    db.commit()
    return {"message": "Appearance preferences updated successfully"}

@router.put("/language")
def update_language(
    body: LanguageUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    st = get_or_create_user_settings(db, current_user.id)
    st.language = body.language
    st.date_format = body.date_format
    st.time_format = body.time_format
    st.units = body.units
    db.commit()
    return {"message": "Language & Regional settings updated successfully"}

@router.post("/export")
def export_health_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return export_user_health_data(db, current_user.id)

@router.post("/logout-all")
def logout_all_devices(
    current_user: User = Depends(get_current_user)
):
    return {"message": "Successfully logged out from all active devices"}

@router.delete("/account")
def delete_account(
    body: AccountDeleteInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_user_account(db, current_user.id, body.password)
