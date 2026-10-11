import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import (
    students_router,
    exams_router,
    questions_router,
    attempts_router,
    analytics_router,
    flashcards_router,
    comparison_router,
    export_router
)

# Create tables if not existing
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Examination Analytics Tool API",
    description="Backend API for college exam evaluation, analytics, flashcards, and DSA algorithms.",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api
app.include_router(students_router, prefix="/api")
app.include_router(exams_router, prefix="/api")
app.include_router(questions_router, prefix="/api")
app.include_router(attempts_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(flashcards_router, prefix="/api")
app.include_router(comparison_router, prefix="/api")
app.include_router(export_router, prefix="/api")

@app.get("/")
def root():
    return {
        "name": "Online Examination Analytics Tool API",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "healthy"}
