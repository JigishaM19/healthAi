from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, HealthProfile
from schemas import HealthProfileSchema, HealthProfileResponse, HealthSummary
from auth import get_current_user

router = APIRouter(tags=["Onboarding & Health Profile"])

def compute_health_summary(profile: HealthProfile) -> HealthSummary:
    # 1. BMI Calculation
    height_m = (profile.height_cm or 170.0) / 100.0
    weight_kg = profile.weight_kg or 70.0
    bmi = round(weight_kg / (height_m * height_m), 1) if height_m > 0 else 22.0

    if bmi < 18.5:
        bmi_cat = "Underweight"
    elif 18.5 <= bmi < 24.9:
        bmi_cat = "Normal weight"
    elif 25.0 <= bmi < 29.9:
        bmi_cat = "Overweight"
    else:
        bmi_cat = "Obese"

    # 2. Health Score Algorithm (0 - 100)
    score = 85
    sleep = profile.sleep_hours or 7.5
    if sleep < 6 or sleep > 9:
        score -= 7
    elif 7.0 <= sleep <= 8.5:
        score += 5

    water = profile.water_intake or 2.5
    if water >= 2.5:
        score += 4
    elif water < 1.5:
        score -= 5

    activity = (profile.activity_level or "moderate").lower()
    if "active" in activity:
        score += 6
    elif "sedentary" in activity:
        score -= 8

    stress = profile.stress_level or 3
    if stress >= 4:
        score -= 10
    elif stress <= 2:
        score += 4

    if profile.conditions:
        score -= (len(profile.conditions) * 4)

    if profile.smoking_status and profile.smoking_status.lower() not in ["never", "no"]:
        score -= 10

    health_score = max(35, min(98, score))

    # 3. Targets and Recommendations
    water_goal = f"{max(2.5, round(weight_kg * 0.035, 1))} Liters / day"
    sleep_target = "7.5 - 8.5 Hours of restorative sleep"
    
    if "active" in activity:
        act_rec = "10,000 steps or 45 mins cardio daily"
    elif "light" in activity or "moderate" in activity:
        act_rec = "8,000 steps or 30 mins brisk walking daily"
    else:
        act_rec = "5,000 steps or 20 mins light movement daily"

    wellness_focus = []
    if sleep < 7.0:
        wellness_focus.append("Improve sleep duration and bedtime consistency")
    if stress >= 3:
        wellness_focus.append("Reduce daily stress via mindfulness & breathing exercises")
    if bmi >= 25.0:
        wellness_focus.append("Maintain caloric balance and low-glycemic nutrition")
    if not wellness_focus:
        wellness_focus.append("Maintain optimal cardiovascular endurance & hydration")

    first_prompt = "How can I optimize my energy levels and daily wellness routine?"
    if profile.conditions:
        first_prompt = f"What wellness steps should I take considering my {profile.conditions[0]}?"

    return HealthSummary(
        bmi=bmi,
        bmi_category=bmi_cat,
        health_score=health_score,
        activity_recommendation=act_rec,
        sleep_target=sleep_target,
        hydration_goal=water_goal,
        personalized_wellness_focus=wellness_focus,
        suggested_consultation=first_prompt
    )


@router.post("/onboarding", response_model=HealthProfileResponse)
def save_onboarding(profile_data: HealthProfileSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    
    if not profile:
        profile = HealthProfile(user_id=current_user.id)
        db.add(profile)

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    # Automatic Timeline Event Generation
    try:
        from services.timeline_service import create_event
        create_event(
            db, 
            current_user.id, 
            "profile", 
            "Health Profile Completed / Updated",
            f"Configured personal health profile: Age {profile.age or 30}, Height {profile.height_cm or 170}cm, Weight {profile.weight_kg or 70}kg.",
            details={"conditions": profile.conditions or [], "medications": profile.medications or []}
        )
    except Exception as e:
        print("Timeline event creation skipped:", e)

    return profile


@router.get("/health-profile", response_model=HealthProfileResponse)
def get_health_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile not created yet. Please complete onboarding."
        )
    return profile


@router.put("/health-profile", response_model=HealthProfileResponse)
def update_health_profile(profile_data: HealthProfileSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return save_onboarding(profile_data, current_user, db)


@router.get("/health-summary", response_model=HealthSummary)
def get_health_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    if not profile:
        # Fallback profile defaults
        profile = HealthProfile(user_id=current_user.id, age=30, height_cm=170.0, weight_kg=70.0)
    return compute_health_summary(profile)
