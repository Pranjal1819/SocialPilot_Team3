# app/schemas/social_account.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# --------------------------------------
# Supported Social Platforms
# --------------------------------------


class SocialPlatform(str, Enum):

    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"


# --------------------------------------
# Base Schema
# --------------------------------------


class SocialAccountBase(BaseModel):

    platform: SocialPlatform

    account_name: str = Field(..., min_length=1, max_length=200)

    account_id: Optional[str] = Field(None, max_length=200)

    is_connected: bool = True


# --------------------------------------
# Create Social Account
# --------------------------------------


class SocialAccountCreate(SocialAccountBase):

    access_token: Optional[str] = None

    refresh_token: Optional[str] = None

    token_expires_at: Optional[datetime] = None


# --------------------------------------
# Update Social Account
# --------------------------------------


class SocialAccountUpdate(BaseModel):

    account_name: Optional[str] = None

    account_id: Optional[str] = None

    is_connected: Optional[bool] = None

    is_active: Optional[bool] = None

    token_expires_at: Optional[datetime] = None


# --------------------------------------
# Response Schema
# --------------------------------------


class SocialAccountResponse(SocialAccountBase):

    id: int

    user_id: int

    is_active: bool

    token_expires_at: Optional[datetime] = None

    created_at: datetime

    updated_at: Optional[datetime] = None

    class Config:

        from_attributes = True


# --------------------------------------
# OAuth Connect Request
# --------------------------------------


class SocialAccountConnect(BaseModel):

    platform: SocialPlatform

    auth_code: str

    redirect_uri: Optional[str] = None


# --------------------------------------
# OAuth Refresh Token Request
# --------------------------------------


class SocialAccountRefresh(BaseModel):

    account_id: int

    refresh_token: str


# --------------------------------------
# OAuth Connect Response
# --------------------------------------


class SocialAccountConnectResponse(BaseModel):

    message: str

    account: Optional[SocialAccountResponse] = None


# --------------------------------------
# OAuth URL Response
# --------------------------------------


class OAuthURLResponse(BaseModel):

    platform: SocialPlatform

    auth_url: str

    redirect_uri: str


# --------------------------------------
# OAuth Callback Response
# --------------------------------------


class OAuthCallbackResponse(BaseModel):

    success: bool

    message: str

    account_id: Optional[int] = None

    platform: Optional[SocialPlatform] = None

    account_name: Optional[str] = None


# --------------------------------------
# Platform Display Information
# --------------------------------------


class PlatformInfo(BaseModel):

    platform: SocialPlatform

    name: str

    icon: str

    is_connected: bool = False

    account_name: Optional[str] = None


# --------------------------------------
# Account Summary
# Used for dropdown/select account
# --------------------------------------


class SocialAccountSummary(BaseModel):

    id: int

    platform: SocialPlatform

    account_name: str

    is_connected: bool

    is_active: bool

    class Config:

        from_attributes = True
