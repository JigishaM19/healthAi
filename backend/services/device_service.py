import hashlib
import datetime
from sqlalchemy.orm import Session
from models import User, TrustedDevice

def generate_device_fingerprint(user_agent: str, ip_address: str) -> str:
    raw = f"{user_agent}|{ip_address}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def parse_user_agent(user_agent: str):
    ua = user_agent.lower()
    browser = "Unknown Browser"
    if "chrome" in ua and "edg" not in ua:
        browser = "Chrome"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Safari"
    elif "firefox" in ua:
        browser = "Firefox"
    elif "edg" in ua:
        browser = "Edge"

    os_name = "Unknown OS"
    if "windows" in ua:
        os_name = "Windows"
    elif "mac" in ua:
        os_name = "macOS"
    elif "android" in ua:
        os_name = "Android"
    elif "iphone" in ua or "ipad" in ua:
        os_name = "iOS"
    elif "linux" in ua:
        os_name = "Linux"

    return browser, os_name

def check_and_register_device(db: Session, user_id: int, user_agent: str, ip_address: str):
    fingerprint = generate_device_fingerprint(user_agent or "default", ip_address or "127.0.0.1")
    browser, os_name = parse_user_agent(user_agent or "")

    device = db.query(TrustedDevice).filter(
        TrustedDevice.user_id == user_id,
        TrustedDevice.device_fingerprint == fingerprint
    ).first()

    is_new = False
    if not device:
        is_new = True
        device = TrustedDevice(
            user_id=user_id,
            device_fingerprint=fingerprint,
            ip_address=ip_address,
            browser=browser,
            operating_system=os_name,
            location="Local Workspace",
            trusted=1,
            last_used_at=datetime.datetime.utcnow()
        )
        db.add(device)
    else:
        device.last_used_at = datetime.datetime.utcnow()

    # Update User last login info
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.last_login_ip = ip_address
        user.last_login_device = f"{browser} on {os_name}"
        user.last_login_at = datetime.datetime.utcnow()

    db.commit()
    return {
        "is_new_device": is_new,
        "device_info": f"{browser} on {os_name}",
        "ip_address": ip_address
    }
