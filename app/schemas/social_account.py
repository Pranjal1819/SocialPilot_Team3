# app/schemas/social_account.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class SocialPlatform(str, Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"

class SocialAccountBase(BaseModel):
    platform: SocialPlatform
    account_name: str = Field(..., min_length=1, max_length=200)
    account_id: Optional[str] = Field(None, max_length=200)
    is_connected: bool = True

class SocialAccountCreate(SocialAccountBase):
    user_id: int
    access_token: Optional[str] = Field(None, max_length=500)
    refresh_token: Optional[str] = Field(None, max_length=500)

class SocialAccountUpdate(BaseModel):
    account_name: Optional[str] = None
    account_id: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    is_connected: Optional[bool] = None

class SocialAccountResponse(SocialAccountBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SocialAccountConnect(BaseModel):
    platform: SocialPlatform
    auth_code: str
    redirect_uri: Optional[str] = None

class SocialAccountRefresh(BaseModel):
    account_id: int
    refresh_token: str

class SocialAccountConnectResponse(BaseModel):
    message: str
    account: Optional[SocialAccountResponse] = None