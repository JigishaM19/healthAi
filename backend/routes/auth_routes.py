from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User, HealthProfile
from schemas import UserSignup, UserLogin, TokenResponse, UserResponse
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Dispatch account_created notification asynchronously
    try:
        from services.notification_service import dispatch_notification
        await dispatch_notification(db, new_user.id, "account_created", {})
    except Exception as ne:
        print("[AuthRoutes] Signup notification error:", ne)

    token = create_access_token({"sub": str(new_user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "has_profile": False,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Register device and check if new device login
    try:
        from services.device_service import check_and_register_device
        from services.notification_service import dispatch_notification
        ua = request.headers.get("user-agent", "Unknown Device")
        ip = request.client.host if request.client else "127.0.0.1"
        dev_res = check_and_register_device(db, user.id, ua, ip)
        if dev_res.get("is_new_device"):
            await dispatch_notification(db, user.id, "new_device_login", dev_res)
    except Exception as de:
        print("[AuthRoutes] Device login check error:", de)

    has_profile = user.health_profile is not None
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "has_profile": has_profile,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "has_profile": current_user.health_profile is not None
    }

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"}
