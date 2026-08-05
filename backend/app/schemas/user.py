# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# =====================================================
# User Roles
# =====================================================


class UserRole(str, Enum):
    ADMIN = "admin"
    BUSINESS = "business_user"
    MARKETING = "marketing_team"
    CONTENT_CREATOR = "content_creator"


# =====================================================
# Common User Schema
# =====================================================


class UserBase(BaseModel):

    email: EmailStr

    name: str = Field(..., min_length=1, max_length=100)

    role: UserRole


# =====================================================
# Email/Password Registration
# =====================================================


class UserCreate(UserBase):

    password: str = Field(..., min_length=6)


# =====================================================
# OAuth Registration
# LinkedIn / Google
# =====================================================


class UserCreateOAuth(BaseModel):
    """
    For OAuth user creation
    """

    email: EmailStr

    name: str

    linkedin_id: Optional[str] = None

    profile_picture: Optional[str] = None

    role: UserRole


# =====================================================
# Login
# =====================================================


class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =====================================================
# Update User
# =====================================================


class UserUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None

    profile_picture: Optional[str] = None

    is_active: Optional[bool] = None

    role: Optional[UserRole] = None


# =====================================================
# User Response
# =====================================================


class UserResponse(UserBase):

    id: int

    profile_picture: Optional[str] = None

    linkedin_id: Optional[str] = None

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Frontend Profile Response
# =====================================================


class UserProfileResponse(BaseModel):
    """
    Extended user profile response
    """

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


# =====================================================
# JWT Token Response
# =====================================================


class Token(BaseModel):
    access_token: str
    token_type: str

    user_id: int
    name: str
    email: str
    role: UserRole


# =====================================================
# JWT Token Data
# =====================================================


class TokenData(BaseModel):

    username: Optional[str] = None

    user_id: Optional[int] = None
