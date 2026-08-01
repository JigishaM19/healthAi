import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from models import User, NotificationLog
from services.email_service import send_email
from services.sms_service import send_sms
from services.timeline_service import create_event

async def dispatch_notification(
    db: Session,
    user_id: int,
    event: str,
    data: Optional[Dict[str, Any]] = None
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return

    data = data or {}
    data["user_name"] = user.name
    email_sent = False
    sms_sent = False

    # Event specific subject & templates
    if event == "account_created":
        email_sent = await send_email(user.email, "Welcome to HealthAI", "account_created.html", data)
        sms_sent = await send_sms(user.phone_number, f"HealthAI: Welcome {user.name}! Your account has been created successfully.")
    
    elif event == "email_verification":
        email_sent = await send_email(user.email, "Verify Your HealthAI Account Email", "email_verification.html", data)
    
    elif event == "phone_verification":
        sms_sent = await send_sms(user.phone_number, f"HealthAI Verification: Your 6-digit OTP code is {data.get('otp_code')}. Valid for 10 minutes.")
    
    elif event == "email_verified":
        sms_sent = await send_sms(user.phone_number, "HealthAI: Your email address has been verified successfully.")
        create_event(db, user_id, "profile", "Email Address Verified", "Your primary email address was verified successfully.")

    elif event == "phone_verified":
        sms_sent = await send_sms(user.phone_number, "HealthAI: Your mobile number has been verified successfully.")
        create_event(db, user_id, "profile", "Mobile Number Verified", "Your mobile number was verified successfully.")

    elif event == "new_device_login":
        email_sent = await send_email(user.email, "Security Alert: New Login to Your HealthAI Account", "new_device_login.html", data)
        create_event(db, user_id, "profile", "New Device Login", f"Login detected from {data.get('device_info')} (IP: {data.get('ip_address')}).")

    elif event == "password_changed":
        email_sent = await send_email(user.email, "Security Alert: Your HealthAI Password Was Changed", "account_created.html", {"title": "Password Changed", "summary": "Your password was updated successfully."})
        sms_sent = await send_sms(user.phone_number, "HealthAI: Your account password has been changed.")
        create_event(db, user_id, "profile", "Password Changed", "Your account security password was updated.")

    elif event == "document_uploaded":
        email_sent = await send_email(user.email, f"Document Uploaded: {data.get('file_name')}", "report_analyzed.html", {"title": "Document Uploaded", "summary": f"{data.get('file_name')} has been uploaded and queued for AI analysis.", "file_name": data.get('file_name')})
        sms_sent = await send_sms(user.phone_number, f"HealthAI: Your medical document '{data.get('file_name')}' has been uploaded and is being analyzed.")

    elif event == "report_analyzed":
        email_sent = await send_email(user.email, f"Report Analysis Complete: {data.get('file_name')}", "report_analyzed.html", data)
        sms_sent = await send_sms(user.phone_number, f"HealthAI: Analysis complete for '{data.get('file_name')}'. View findings in your portal.")

    elif event == "medication_reminder":
        sms_sent = await send_sms(user.phone_number, f"HealthAI Reminder: Time to take {data.get('medication_name', 'your prescribed medication')}.")
        create_event(db, user_id, "medication", "Medication Reminder Sent", f"Reminder sent for {data.get('medication_name')}.")

    elif event == "appointment_reminder":
        sms_sent = await send_sms(user.phone_number, f"HealthAI Reminder: Doctor appointment scheduled for {data.get('appointment_time', 'tomorrow')}.")
        create_event(db, user_id, "wellness", "Appointment Reminder Sent", f"Follow-up appointment on {data.get('appointment_time')}.")

    elif event == "critical_health_alert":
        email_sent = await send_email(user.email, "URGENT HEALTH ALERT: Critical Value Detected", "new_device_login.html", {"title": "Critical Value Detected", "summary": data.get("alert_message", "Critical lab marker detected.")})
        sms_sent = await send_sms(user.phone_number, f"HealthAI Alert: Critical lab result detected in your report. Please review immediately.")
        create_event(db, user_id, "report", "Critical Health Alert", data.get("alert_message", "Critical value detected."))

    elif event == "account_deleted":
        email_sent = await send_email(user.email, "Account Deleted", "account_created.html", {"title": "Account Deleted", "summary": "Your HealthAI account and records were deleted."})
        sms_sent = await send_sms(user.phone_number, "HealthAI: Your account has been deleted successfully.")

    # Log Email notification
    if email_sent:
        log_e = NotificationLog(
            user_id=user_id,
            channel="email",
            event=event,
            recipient=user.email,
            status="sent",
            sent_at=datetime.datetime.utcnow()
        )
        db.add(log_e)

    # Log SMS notification
    if sms_sent:
        log_s = NotificationLog(
            user_id=user_id,
            channel="sms",
            event=event,
            recipient=user.phone_number or "SMS Provider",
            status="sent",
            sent_at=datetime.datetime.utcnow()
        )
        db.add(log_s)

    db.commit()
