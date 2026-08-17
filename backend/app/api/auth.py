# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import requests
from typing import Optional
import hashlib
from datetime import datetime

from app.models.login_device import LoginDevice

from app.core.dependencies import get_current_user
from app.core.database import get_db

from app.core.security import verify_password, get_password_hash, create_access_token

from app.models.user import User

from app.schemas.user import UserCreate, UserResponse, Token, UserRole, PasswordChange
from app.services.notification_service import NotificationService
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ============================================================
# LinkedIn OAuth
# ============================================================


@router.get("/linkedin/login")
def linkedin_login(redirect_uri: Optional[str] = None):

    frontend_redirect = redirect_uri or settings.LINKEDIN_REDIRECT_URI_FRONTEND

    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": "openid profile email",
        "state": frontend_redirect,
    }

    linkedin_url = "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(
        params
    )

    return RedirectResponse(url=linkedin_url)


@router.get("/linkedin/callback")
def linkedin_callback(
    code: Optional[str] = None,
    error: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):

    frontend_url = state or settings.LINKEDIN_REDIRECT_URI_FRONTEND

    if error:
        return RedirectResponse(url=f"{frontend_url}?error={error}")

    if not code:
        return RedirectResponse(url=f"{frontend_url}?error=missing_code")

    try:

        token_response = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            },
        )

        token_json = token_response.json()

        access_token = token_json.get("access_token")

        if not access_token:
            return RedirectResponse(url=f"{frontend_url}?error=no_access_token")

        user_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user_response.status_code != 200:
            return RedirectResponse(url=f"{frontend_url}?error=userinfo_failed")

        user_data = user_response.json()

        linkedin_id = user_data.get("sub")
        email = user_data.get("email")
        name = user_data.get("name")
        picture = user_data.get("picture")

        if not linkedin_id or not email:
            return RedirectResponse(url=f"{frontend_url}?error=missing_user_data")

        user = db.query(User).filter(User.linkedin_id == linkedin_id).first()

        if not user:

            user = db.query(User).filter(User.email == email).first()

            if user:

                user.linkedin_id = linkedin_id

                if picture:
                    user.profile_picture = picture

                db.commit()
                db.refresh(user)

            else:

                user = User(
                    email=email,
                    name=name,
                    linkedin_id=linkedin_id,
                    profile_picture=picture,
                    password=None,
                    role=UserRole.CONTENT_CREATOR.value,
                    is_active=True,
                )

                db.add(user)

                db.commit()

                db.refresh(user)

        jwt_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role,
            }
        )

        redirect_url = f"{frontend_url}" f"?token={jwt_token}" f"&user_id={user.id}"

        return RedirectResponse(url=redirect_url)

    except Exception as e:

        print(f"LinkedIn OAuth error: {str(e)}")

        return RedirectResponse(url=f"{frontend_url}?error={str(e)}")


# ============================================================
# Registration
# ============================================================


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Only one admin allowed

    if user.role == UserRole.ADMIN:

        admin_exists = db.query(User).filter(User.role == UserRole.ADMIN.value).first()

        if admin_exists:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrator account already exists",
            )

    db_user = User(
        email=user.email,
        name=user.name,
        password=get_password_hash(user.password),
        role=user.role.value,
        is_active=True,
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


# ============================================================
# Available Registration Roles
# ============================================================


@router.get("/available-roles")
def available_roles(db: Session = Depends(get_db)):
    """
    Returns roles available for registration.

    Before first admin creation:
        admin
        business_user
        marketing_team
        content_creator


    After admin creation:
        business_user
        marketing_team
        content_creator
    """

    admin_exists = db.query(User).filter(User.role == UserRole.ADMIN.value).first()

    if admin_exists:

        return {"roles": ["business_user", "marketing_team", "content_creator"]}

    return {"roles": ["admin", "business_user", "marketing_team", "content_creator"]}


# ============================================================
# Login
# ============================================================


@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:

        print("========== LOGIN REQUEST ==========")
        print("Email:", form_data.username)

        user = db.query(User).filter(User.email == form_data.username).first()

        if not user:
            print("User not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        print("User found:", user.name)

        if not user.password:
            print("Password is None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password login not available for this account",
            )

        if not verify_password(form_data.password, user.password):
            print("Password verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            print("User inactive")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated",
            )

        # --------------------------------------------------
        # New-device detection
        # --------------------------------------------------

        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        fingerprint = hashlib.sha256(
            f"{client_ip}:{user_agent}".encode()
        ).hexdigest()

        device = (
            db.query(LoginDevice)
            .filter(
                LoginDevice.user_id == user.id,
                LoginDevice.fingerprint == fingerprint,
            )
            .first()
        )

        if device:

            device.last_seen_at = datetime.utcnow()
            db.commit()

        else:

            device = LoginDevice(
                user_id=user.id,
                fingerprint=fingerprint,
                ip_address=client_ip,
                user_agent=user_agent,
            )

            db.add(device)
            db.commit()

            NotificationService(db).create_notification(
                user_id=user.id,
                title="New Device Login",
                description=f"Your account was logged in from a new device (IP: {client_ip}).",
                category="account",
                notification_type="new_device_login",
            )

        print("Creating JWT token...")

        token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role,
            }
        )

        print("JWT created successfully")
        print("Returning response...")

        response = {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

        print(response)
        print("========== LOGIN SUCCESS ==========")

        return response

    except HTTPException:
        raise

    except Exception as e:
        print("========== LOGIN ERROR ==========")
        print(type(e))
        print(e)
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
# ============================================================
# Change Password
# ============================================================


@router.patch("/change-password")
def change_password(
    payload: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if not current_user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password login not available for this account",
        )

    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    current_user.password = get_password_hash(payload.new_password)

    db.commit()

    NotificationService(db).create_notification(
        user_id=current_user.id,
        title="Password Changed",
        description="Your account password was changed successfully.",
        category="account",
        notification_type="password_changed",
    )

    return {"message": "Password changed successfully"}

# ============================================================
# Current User
# ============================================================


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):

    return current_user


# ============================================================
# Logout
# ============================================================


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):

    return {"message": "Logged out successfully"}


# ============================================================
# Refresh Token
# ============================================================


@router.post("/refresh", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_user)):

    token = create_access_token(
        data={"sub": current_user.email, "user_id": current_user.id}
    )

    return {"access_token": token, "token_type": "bearer"}
