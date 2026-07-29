# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    BUSINESS = "business_user"
    MARKETING = "marketing_team"
    CONTENT_CREATOR = "content_creator"
    USER = "user"

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: Optional[UserRole] = UserRole.USER

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserCreateOAuth(BaseModel):
    """For OAuth user creation (LinkedIn, Google, etc.)"""
    email: EmailStr
    name: str
    linkedin_id: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class UserResponse(UserBase):
    id: int
    profile_picture: Optional[str] = None
    linkedin_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    """Extended user profile for frontend"""
    id: int
    email: str
    name: str
    role: str
    profile_picture: Optional[str] = None
    is_active: bool
    created_at: datetime
    linkedin_connected: bool = False
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None