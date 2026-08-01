import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth_routes, onboarding_routes, chat_routes, user_routes, timeline_routes, report_routes, memory_routes, settings_routes, verification_routes, nutrition_routes

# Automatically create SQLite/PostgreSQL database tables on server start
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HealthAI API",
    description="Production-Ready AI Health Assistant API with Clinical Triage & Health Profile context",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_routes.router)
app.include_router(onboarding_routes.router)
app.include_router(chat_routes.router)
app.include_router(user_routes.router)
app.include_router(timeline_routes.router)
app.include_router(report_routes.router)
app.include_router(memory_routes.router)
app.include_router(settings_routes.router)
app.include_router(verification_routes.router)
app.include_router(nutrition_routes.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "app": "HealthAI Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
