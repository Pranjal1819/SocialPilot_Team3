from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

# ==================================================
# User Roles
# ==================================================


class UserRole(str, Enum):
    ADMIN = "administrator"
    BUSINESS_USER = "business_user"
    MARKETING_TEAM = "marketing_team"
    CONTENT_CREATOR = "content_creator"


# ==================================================
# Base User Schema
# ==================================================


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    organization: Optional[str] = None
    designation: Optional[str] = None
    bio: Optional[str] = None


# ==================================================
# Registration
# ==================================================


class UserCreate(UserBase):
    password: str
    role: UserRole


# ==================================================
# Login
# ==================================================


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ==================================================
# Change Password
# ==================================================


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


# ==================================================
# Update Profile
# ==================================================


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    designation: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


# ==================================================
# User Response
# ==================================================


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================================================
# User Profile Response
# ==================================================


class UserProfileResponse(UserResponse):
    profile_picture: Optional[str] = None


# ==================================================
# JWT Token
# ==================================================


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    name: str
    email: str
    role: str


# ==================================================
# Token Data
# ==================================================


class TokenData(BaseModel):
    email: Optional[str] = None
