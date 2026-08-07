# app/main.py

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api import auth, posts, campaigns, social, analytics, admin
from app.api import business_assignment, business_management


app = FastAPI(
    title="SocialPilot API",
    description="Social Media Scheduling & Campaign Management Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve locally-uploaded post media (images/videos/audio/documents)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(campaigns.router)
app.include_router(social.router)
app.include_router(analytics.router)
app.include_router(admin.router)

app.include_router(business_assignment.router)
app.include_router(business_management.router)


@app.get("/")
def root():
    return {"message": "SocialPilot API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
