from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, HealthProfile, Conversation, Message
from schemas import ChatMessageInput, ChatResponse, ConversationResponse
from auth import get_current_user
from services.ai_service import generate_health_guidance

router = APIRouter(tags=["AI Health Consultation Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_consultation(
    input_data: ChatMessageInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Fetch user's health profile
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    profile_dict = {}
    if profile:
        profile_dict = {
            "age": profile.age,
            "gender": profile.gender,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "conditions": profile.conditions or [],
            "allergies": profile.allergies or [],
            "medications": profile.medications or [],
            "goals": profile.goals or [],
            "activity_level": profile.activity_level,
            "stress_level": profile.stress_level,
            "mood": profile.mood
        }

    # 2. Retrieve or create Conversation
    if input_data.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == input_data.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Title snippet from first 30 chars
        title_text = input_data.message[:35] + ("..." if len(input_data.message) > 35 else "")
        conversation = Conversation(user_id=current_user.id, title=title_text)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 3. Format previous messages for AI context
    history_msgs = []
    past_messages = db.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.timestamp.asc()).all()
    for m in past_messages:
        history_msgs.append({"role": m.role, "content": m.content})

    # Save user message
    user_msg_db = Message(
        conversation_id=conversation.id,
        role="user",
        content=input_data.message
    )
    db.add(user_msg_db)
    db.commit()

    # 4. Build Health Memory & Nutrition Prompt Context
    from services.health_memory_service import build_memory_prompt_context, create_memory_entry
    memory_context = build_memory_prompt_context(db, current_user.id, input_data.message)

    # Detect Nutrition Intent
    nut_keywords = [
        "lose weight", "weight loss", "gain weight", "diet", "meal plan", "calories",
        "protein", "carbohydrates", "fat loss", "obesity", "diabetes diet", "hypertension diet",
        "thyroid diet", "pcos diet", "kidney diet", "liver diet", "cholesterol diet",
        "vegetarian", "vegan", "jain diet", "fasting", "healthy eating", "what to eat", "grocery"
    ]
    msg_lower = input_data.message.lower()
    if any(k in msg_lower for k in nut_keywords):
        try:
            from services.nutrition_service import generate_personalized_diet_plan
            n_plan = generate_personalized_diet_plan(db, current_user.id, input_data.message)
            t = n_plan.get("targets", {})
            r = n_plan.get("diet_rules", {})
            nut_summary = (
                f"\n\n[PERSONALIZED AI NUTRITION SYSTEM DATA]:\n"
                f"- Daily Calorie Target: {t.get('target_calories')} kcal/day (BMR: {n_plan['metrics']['bmr']}, TDEE: {n_plan['metrics']['tdee']})\n"
                f"- Macro Breakdown: Protein: {t.get('protein_g')}g, Carbs: {t.get('carbs_g')}g, Fat: {t.get('fat_g')}g, Fiber: {t.get('fiber_g')}g\n"
                f"- Hydration Target: {n_plan.get('hydration', {}).get('daily_target_liters', 3.0)} Liters/day\n"
                f"- Foods to Eat: {', '.join(r.get('foods_to_eat', [])[:8])}\n"
                f"- Foods to Avoid: {', '.join(r.get('foods_to_avoid', [])[:8])}\n"
                f"- Sample Day 1 Plan: Breakfast ({n_plan['meal_plan_7day'][0]['breakfast']}), Lunch ({n_plan['meal_plan_7day'][0]['lunch']}), Dinner ({n_plan['meal_plan_7day'][0]['dinner']})\n"
                f"- Recommended Workout: {n_plan.get('workout_plan', {}).get('exercise_type')} ({n_plan.get('workout_plan', {}).get('daily_step_target')} steps/day)"
            )
            memory_context = (memory_context or "") + nut_summary
        except Exception as ne:
            print("[ChatRoutes] Nutrition plan generation error:", ne)

    # 5. Generate AI Health Response incorporating Health Profile & Health Memory
    ai_result = await generate_health_guidance(
        user_message=input_data.message,
        profile_data=profile_dict,
        conversation_history=history_msgs,
        memory_context=memory_context
    )

    # Save assistant message
    assistant_msg_db = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_result["reply"],
        analysis=ai_result["analysis"]
    )
    db.add(assistant_msg_db)
    db.commit()

    # Automatic Timeline Event & Health Memory Generation
    try:
        from services.timeline_service import create_event
        analysis = ai_result.get("analysis", {})
        create_event(
            db,
            current_user.id,
            "consultation",
            f"AI Consultation: {conversation.title}",
            f"Ward: {analysis.get('ward', 'general').upper()} | Specialist: {analysis.get('assigned_doctor', 'Internal Medicine')}",
            details=analysis
        )
        create_memory_entry(
            db,
            current_user.id,
            "consultation",
            f"Consultation: {conversation.title}",
            f"Specialist: {analysis.get('assigned_doctor', 'General')}. Advice: {analysis.get('personalized_advice', '')}",
            source_type="conversation",
            source_id=conversation.id,
            metadata_json=analysis
        )
    except Exception as e:
        print("Timeline consultation event/memory creation skipped:", e)

    return {
        "conversation_id": conversation.id,
        "reply": ai_result["reply"],
        "analysis": ai_result["analysis"]
    }


@router.get("/history", response_model=List[ConversationResponse])
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).all()
    return conversations


@router.delete("/history/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conv)
    db.commit()
    return {"message": "Conversation deleted successfully"}
