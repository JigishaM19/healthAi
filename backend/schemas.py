from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    has_profile: bool
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    has_profile: bool = False

    class Config:
        from_attributes = True

# --- Health Profile Schemas ---
class HealthProfileSchema(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    
    conditions: List[str] = []
    allergies: List[str] = []
    medications: List[str] = []
    surgeries: Optional[str] = None
    pregnancy_status: Optional[str] = None
    
    activity_level: Optional[str] = None
    exercise_frequency: Optional[str] = None
    sleep_hours: Optional[float] = 7.5
    smoking_status: Optional[str] = None
    alcohol_consumption: Optional[str] = None
    water_intake: Optional[float] = 2.5
    diet_type: Optional[str] = None
    
    goals: List[str] = []
    
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    city_country: Optional[str] = None
    preferred_language: Optional[str] = "English"
    family_history: List[str] = []
    notification_preferences: Dict[str, bool] = {}
    
    stress_level: Optional[int] = 3
    mood: Optional[str] = "Calm"

    class Config:
        from_attributes = True

class HealthProfileResponse(HealthProfileSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

# --- Computed Dashboard Summary ---
class HealthSummary(BaseModel):
    bmi: float
    bmi_category: str
    health_score: int
    activity_recommendation: str
    sleep_target: str
    hydration_goal: str
    personalized_wellness_focus: List[str]
    suggested_consultation: str

# --- Chat Schemas ---
class ChatMessageInput(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class AIAnalysisCard(BaseModel):
    possible_causes: List[str]
    recommended_actions: List[str]
    warning_signs: List[str]
    personalized_advice: str
    confidence: float
    ward: str = "general"
    assigned_doctor: Optional[str] = None

class ChatMessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    analysis: Optional[AIAnalysisCard] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    analysis: AIAnalysisCard

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True
