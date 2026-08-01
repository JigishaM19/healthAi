from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from database import get_db
from models import User, NotificationLog, TrustedDevice
from auth import get_current_user
from services.verification_service import (
    generate_email_verification_token,
    generate_phone_otp,
    verify_email_token,
    verify_phone_otp
)
from services.notification_service import dispatch_notification
from services.reminder_service import send_medication_reminder, send_appointment_reminder, get_active_reminders
from services.device_service import check_and_register_device

router = APIRouter(tags=["Verification, Notifications & Devices"])

class SendOtpInput(BaseModel):
    phone_number: str

class VerifyOtpInput(BaseModel):
    otp_code: str

class TestNotificationInput(BaseModel):
    subject: Optional[str] = "HealthAI Test Notification"
    message: Optional[str] = "This is a test notification from HealthAI."

class ReminderInput(BaseModel):
    medication_name: Optional[str] = "Amlodipine 5 mg"
    doctor_name: Optional[str] = "Dr. Elena Rostova"
    appointment_time: Optional[str] = "Tomorrow at 10:30 AM"

class TrustDeviceInput(BaseModel):
    device_id: int


# --- Verification Endpoints ---

@router.post("/verification/send-email")
async def send_verification_email_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    token = generate_email_verification_token(db, current_user.id)
    app_url = "http://localhost:3000"
    url = f"{app_url}/verification/email/{token}"

    await dispatch_notification(db, current_user.id, "email_verification", {
        "verification_url": url
    })
    return {"message": "Verification email sent successfully", "token": token}


@router.get("/verification/email/{token}")
async def verify_email_route(
    token: str,
    db: Session = Depends(get_db)
):
    user = verify_email_token(db, token)
    await dispatch_notification(db, user.id, "email_verified", {})
    return {"message": "Email address verified successfully!", "user_id": user.id}


@router.post("/verification/send-otp")
async def send_otp_route(
    body: SendOtpInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    otp = generate_phone_otp(db, current_user.id, body.phone_number)
    await dispatch_notification(db, current_user.id, "phone_verification", {
        "otp_code": otp
    })
    return {"message": "6-digit OTP code sent via SMS", "otp_code": otp}


@router.post("/verification/verify-otp")
async def verify_otp_route(
    body: VerifyOtpInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = verify_phone_otp(db, current_user.id, body.otp_code)
    await dispatch_notification(db, user.id, "phone_verified", {})
    return {"message": "Mobile number verified successfully!", "user_id": user.id}


# --- Notifications Endpoints ---

@router.post("/notifications/test-email")
async def test_email_route(
    body: TestNotificationInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    await dispatch_notification(db, current_user.id, "account_created", {
        "title": body.subject,
        "summary": body.message
    })
    return {"message": "Test email sent successfully"}


@router.post("/notifications/test-sms")
async def test_sms_route(
    body: TestNotificationInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    await dispatch_notification(db, current_user.id, "medication_reminder", {
        "medication_name": body.message
    })
    return {"message": "Test SMS sent successfully"}


@router.get("/notifications/history")
def notification_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = db.query(NotificationLog).filter(
        NotificationLog.user_id == current_user.id
    ).order_by(NotificationLog.sent_at.desc()).limit(50).all()
    return logs


# --- Device Management Endpoints ---

@router.get("/devices")
def list_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    devices = db.query(TrustedDevice).filter(
        TrustedDevice.user_id == current_user.id
    ).order_by(TrustedDevice.last_used_at.desc()).all()
    return devices


@router.delete("/devices/{id}")
def delete_device(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dev = db.query(TrustedDevice).filter(
        TrustedDevice.id == id,
        TrustedDevice.user_id == current_user.id
    ).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Device not found")

    db.delete(dev)
    db.commit()
    return {"message": "Device removed from trusted devices"}


@router.post("/devices/trust")
def trust_device(
    body: TrustDeviceInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dev = db.query(TrustedDevice).filter(
        TrustedDevice.id == body.device_id,
        TrustedDevice.user_id == current_user.id
    ).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Device not found")

    dev.trusted = 1
    db.commit()
    return {"message": "Device marked as trusted"}


# --- Reminders Endpoints ---

@router.post("/reminders/medication")
async def trigger_medication_reminder(
    body: ReminderInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await send_medication_reminder(db, current_user.id, body.medication_name or "Amlodipine 5 mg")


@router.post("/reminders/appointment")
async def trigger_appointment_reminder(
    body: ReminderInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await send_appointment_reminder(
        db, current_user.id,
        body.doctor_name or "Dr. Elena Rostova",
        body.appointment_time or "Tomorrow at 10:30 AM"
    )


@router.get("/reminders")
def list_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_active_reminders(db, current_user.id)
