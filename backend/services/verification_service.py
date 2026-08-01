import secrets
import random
import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, VerificationToken

def generate_email_verification_token(db: Session, user_id: int) -> str:
    token = secrets.token_hex(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=24)

    record = VerificationToken(
        user_id=user_id,
        token=token,
        verification_type="email",
        expires_at=expires_at,
        used=0
    )
    db.add(record)
    db.commit()
    return token

def generate_phone_otp(db: Session, user_id: int, phone_number: str) -> str:
    otp = f"{random.randint(100000, 999999)}"
    token = secrets.token_hex(16)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    # Save phone_number to user record
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.phone_number = phone_number

    record = VerificationToken(
        user_id=user_id,
        token=token,
        verification_type="phone",
        otp_code=otp,
        expires_at=expires_at,
        used=0
    )
    db.add(record)
    db.commit()
    return otp

def verify_email_token(db: Session, token: str) -> User:
    vt = db.query(VerificationToken).filter(
        VerificationToken.token == token,
        VerificationToken.verification_type == "email",
        VerificationToken.used == 0
    ).first()

    if not vt:
        raise HTTPException(status_code=400, detail="Invalid or already used verification token")

    if datetime.datetime.utcnow() > vt.expires_at:
        raise HTTPException(status_code=400, detail="Verification token has expired")

    vt.used = 1
    user = db.query(User).filter(User.id == vt.user_id).first()
    if user:
        user.email_verified = 1
        if user.phone_verified:
            user.account_verified = 1

    db.commit()
    db.refresh(user)
    return user

def verify_phone_otp(db: Session, user_id: int, otp_code: str) -> User:
    vt = db.query(VerificationToken).filter(
        VerificationToken.user_id == user_id,
        VerificationToken.verification_type == "phone",
        VerificationToken.otp_code == otp_code,
        VerificationToken.used == 0
    ).order_by(VerificationToken.created_at.desc()).first()

    if not vt:
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    if datetime.datetime.utcnow() > vt.expires_at:
        raise HTTPException(status_code=400, detail="OTP code has expired")

    vt.used = 1
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.phone_verified = 1
        if user.email_verified:
            user.account_verified = 1

    db.commit()
    db.refresh(user)
    return user
