import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthai.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def apply_schema_migrations():
    """Safely adds missing columns to SQLite/PostgreSQL tables."""
    with engine.connect() as conn:
        try:
            # Check user_settings columns
            if DATABASE_URL.startswith("sqlite"):
                cursor = conn.execute(text("PRAGMA table_info(user_settings)"))
                cols = [row[1] for row in cursor.fetchall()]
                if "two_factor_enabled" not in cols:
                    conn.execute(text("ALTER TABLE user_settings ADD COLUMN two_factor_enabled INTEGER DEFAULT 0"))
                if "preferred_2fa_method" not in cols:
                    conn.execute(text("ALTER TABLE user_settings ADD COLUMN preferred_2fa_method VARCHAR DEFAULT 'email'"))
                if "anonymized_research_sharing" not in cols:
                    conn.execute(text("ALTER TABLE user_settings ADD COLUMN anonymized_research_sharing INTEGER DEFAULT 0"))
                conn.commit()
        except Exception as e:
            print("[Database] Schema migration note:", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
