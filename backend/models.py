import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    email_verified = Column(Integer, default=0)
    phone_verified = Column(Integer, default=0)
    account_verified = Column(Integer, default=0)
    last_login_ip = Column(String, nullable=True)
    last_login_device = Column(String, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    health_profile = relationship("HealthProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Step 1: Basic Info
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    
    # Step 2: Medical Background
    conditions = Column(JSON, default=list)       # list of strings
    allergies = Column(JSON, default=list)        # list of strings
    medications = Column(JSON, default=list)      # list of strings
    surgeries = Column(String, nullable=True)
    pregnancy_status = Column(String, nullable=True)
    
    # Step 3: Lifestyle Assessment
    activity_level = Column(String, nullable=True) # e.g. sedentary, light, moderate, active
    exercise_frequency = Column(String, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    smoking_status = Column(String, nullable=True)
    alcohol_consumption = Column(String, nullable=True)
    water_intake = Column(Float, nullable=True)   # in Liters/day
    diet_type = Column(String, nullable=True)
    
    # Step 4: Health Goals
    goals = Column(JSON, default=list)            # list of strings
    
    # Step 5: Risk & Emergency Info + Mental Wellness
    blood_group = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=True)
    city_country = Column(String, nullable=True)
    preferred_language = Column(String, default="English")
    family_history = Column(JSON, default=list)   # list of strings
    notification_preferences = Column(JSON, default=dict)
    
    stress_level = Column(Integer, default=3)     # 1-5 scale
    mood = Column(String, default="Calm")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="health_profile")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, default="Health Consultation")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False) # "user" or "assistant"
    content = Column(Text, nullable=False)
    analysis = Column(JSON, nullable=True) # structured AI analysis card data
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(String, nullable=False, index=True) # "consultation", "report", "medication", "wellness", "profile"
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class MedicalDocument(Base):
    __tablename__ = "medical_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False) # pdf, docx, txt, csv, xlsx, jpg, png, etc.
    document_type = Column(String, default="general_medical", index=True)
    file_path = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    structured_data = Column(JSON, default=dict)
    ai_summary = Column(Text, nullable=True)
    abnormal_values = Column(JSON, default=list)
    pdf_report_path = Column(String, nullable=True)
    pdf_generated = Column(Integer, default=0)
    pdf_generated_at = Column(DateTime, nullable=True)
    analyzed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    medicine_name = Column(String, nullable=False, index=True)
    dosage = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    prescribing_doctor = Column(String, nullable=True)
    active = Column(String, default="active") # "active", "completed", "discontinued"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class LabMeasurement(Base):
    __tablename__ = "lab_measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("medical_documents.id"), nullable=True)
    test_name = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    reference_range = Column(String, nullable=True)
    status = Column(String, nullable=True) # "Low", "Normal", "High", "Critical"
    test_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class HealthMemory(Base):
    __tablename__ = "health_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    memory_type = Column(String, nullable=False, index=True) # "consultation", "lab_report", "prescription", "medication", "wellness", "profile"
    source_type = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    theme = Column(String, default="dark")
    language = Column(String, default="English")
    units = Column(String, default="Metric")
    phone_number = Column(String, nullable=True)
    email_notifications = Column(JSON, default=dict)
    push_notifications = Column(JSON, default=dict)
    medication_reminders = Column(Integer, default=1)
    hydration_reminders = Column(Integer, default=1)
    exercise_reminders = Column(Integer, default=1)
    sleep_reminders = Column(Integer, default=1)
    appointment_reminders = Column(Integer, default=1)
    report_notifications = Column(Integer, default=1)
    date_format = Column(String, default="YYYY-MM-DD")
    time_format = Column(String, default="12h")
    reduce_animations = Column(Integer, default=0)
    high_contrast = Column(Integer, default=0)
    font_size = Column(String, default="medium")
    two_factor_enabled = Column(Integer, default=0)
    preferred_2fa_method = Column(String, default="email")
    anonymized_research_sharing = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    verification_type = Column(String, nullable=False) # "email" or "phone"
    otp_code = Column(String, nullable=True) # 6-digit OTP
    expires_at = Column(DateTime, nullable=False)
    used = Column(Integer, default=0) # 0 or 1
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    channel = Column(String, nullable=False) # "email" or "sms"
    event = Column(String, nullable=False, index=True) # "account_created", "document_uploaded", etc.
    recipient = Column(String, nullable=False)
    status = Column(String, default="sent") # "sent", "failed", "pending"
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)


class TrustedDevice(Base):
    __tablename__ = "trusted_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    device_fingerprint = Column(String, nullable=False, index=True)
    ip_address = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    operating_system = Column(String, nullable=True)
    location = Column(String, nullable=True, default="Unknown Location")
    trusted = Column(Integer, default=1) # 0 or 1
    last_used_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    device = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    os = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    location = Column(String, nullable=True, default="Unknown Location")
    token_id = Column(String, nullable=True)
    is_current = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ConnectedDevice(Base):
    __tablename__ = "connected_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    provider = Column(String, nullable=False, index=True) # "google_fit", "apple_health", "fitbit", "samsung_health"
    account_id = Column(String, nullable=True)
    connected = Column(Integer, default=1) # 1 or 0
    last_sync = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
