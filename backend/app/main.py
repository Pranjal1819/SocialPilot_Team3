# app/main.py

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings

from app.api import (
auth,
posts,
campaigns,
social,
analytics,
admin,
team_activity,
notifications,
reports,
business_assignment,
business_management,
)

from app.api.publishing import router as publishing_router


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
title="SocialPilot API",
description="Social Media Scheduling & Campaign Management Platform",
version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
CORSMiddleware,
allow_origins=[
"http://localhost:3000",
"http://localhost:3001",
],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# =========================================================
# Static Uploads
# =========================================================

os.makedirs(
settings.UPLOAD_DIR,
exist_ok=True,
)

app.mount(
"/uploads",
StaticFiles(
directory=settings.UPLOAD_DIR
),
name="uploads",
)


# =========================================================
# API Routers
# =========================================================

app.include_router(
team_activity.router
)

app.include_router(
auth.router
)

app.include_router(
posts.router
)

app.include_router(
campaigns.router
)

app.include_router(
social.router
)


# =========================================================
# OAuth Callback Routers
#
# YouTube:
# /auth/youtube/callback
#
# Instagram:
# /auth/instagram/callback
# =========================================================

app.include_router(
social.youtube_callback_router
)

app.include_router(
social.instagram_callback_router
)


# =========================================================
# Other Routers
# =========================================================

app.include_router(
analytics.router
)

app.include_router(
admin.router
)

app.include_router(
publishing_router
)

app.include_router(
business_assignment.router
)

app.include_router(
business_management.router
)

app.include_router(
notifications.router
)

app.include_router(
reports.router
)


# =========================================================
# Root
# =========================================================

@app.get("/")
def root():

    return {
"message": "SocialPilot API",
"version": "1.0.0",
"docs": "/docs",
}


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
def health_check():

    return {
"status": "healthy"
}
