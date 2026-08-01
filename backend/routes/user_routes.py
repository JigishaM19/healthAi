from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserResponse
from auth import get_current_user
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(tags=["User Profile"])

class UserUpdateInput(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

@router.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "has_profile": current_user.health_profile is not None
    }

@router.put("/profile", response_model=UserResponse)
def update_user_profile(
    data: UserUpdateInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.name:
        current_user.name = data.name
    if data.email and data.email != current_user.email:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
        current_user.email = data.email

    db.commit()
    db.refresh(current_user)
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "has_profile": current_user.health_profile is not None
    }
