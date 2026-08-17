import secrets
from app.core.config import settings
from app.services.redis_client import get_redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.social_account import SocialAccount

from app.schemas.social_account import (
    SocialAccountUpdate,
    SocialAccountResponse,
    SocialAccountConnect,
    OAuthURLResponse,
    OAuthCallbackResponse,
    PlatformInfo,
    SocialAccountSummary,
)

from app.services.social_integration import SocialIntegrationService
from app.services.social.x import XService
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/api/social",
    tags=["Social Accounts"],
)

# --------------------------------------------------------
# Separate, no-prefix router — ONLY for the YouTube OAuth
# callback. Google Cloud Console has this registered as
# http://localhost:8000/auth/youtube/callback, which does
# NOT match the /api/social/callback/{platform} pattern
# used by every other platform below. Re-registering it
# would need the teammate who owns those credentials, so
# this route matches what's already registered instead.
# --------------------------------------------------------

youtube_callback_router = APIRouter(tags=["Social Accounts"])

REDIRECT_URIS = {
    "linkedin": "http://localhost:8000/api/social/callback/linkedin",
    "x": "http://localhost:8000/api/social/callback/x",
    "facebook": "http://localhost:8000/api/social/callback/facebook",
    "youtube": settings.YOUTUBE_REDIRECT_URI,
}

SUPPORTED_PLATFORMS = [
    "linkedin",
    "facebook",
    "instagram",
    "x",
    "youtube",
]


# ---------------------------------------------------------
# Generate OAuth URL
# ---------------------------------------------------------


@router.get("/auth-url/{platform}", response_model=OAuthURLResponse)
def get_oauth_url(
    platform: str,
    current_user: User = Depends(get_current_user),
):

    platform = platform.lower()

    if platform not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported platform",
        )

    redirect_uri = REDIRECT_URIS.get(platform)

    if not redirect_uri:
        raise HTTPException(
            status_code=400,
            detail=f"No redirect URI configured for {platform}",
        )

    service = SocialIntegrationService(None)

    state = secrets.token_urlsafe(32)

    redis = get_redis()

    redis.setex(
        f"oauth_state:{state}",
        600,
        str(current_user.id),
    )

    code_challenge = None

    if platform == "x":

        x_service = XService()

        code_verifier, code_challenge = x_service.generate_pkce_pair()

        redis.setex(
            f"oauth_verifier:{state}",
            600,
            code_verifier,
        )

    auth_url = service.get_oauth_url(
        platform=platform,
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
    )

    if platform != "x":
        separator = "&" if "?" in auth_url else "?"
        auth_url = f"{auth_url}{separator}state={state}"

    return OAuthURLResponse(
        platform=platform,
        auth_url=auth_url,
        redirect_uri=redirect_uri,
    )


# ---------------------------------------------------------
# Connect Account
# ---------------------------------------------------------


@router.post(
    "/connect",
    response_model=OAuthCallbackResponse,
)
def connect_social_account(
    connect_data: SocialAccountConnect,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    platform = (
        connect_data.platform.lower()
        if isinstance(connect_data.platform, str)
        else connect_data.platform.value
    )

    redirect_uri = connect_data.redirect_uri or REDIRECT_URIS.get(platform)

    service = SocialIntegrationService(db)

    result = service.connect_account(
        platform=platform,
        auth_code=connect_data.auth_code,
        user_id=current_user.id,
        redirect_uri=redirect_uri,
        code_verifier=getattr(connect_data, "code_verifier", None),
    )

    NotificationService(db).create_notification(
        user_id=current_user.id,
        title="Account Connected",
        description=f'Your {platform} account "{result["account_name"]}" was connected successfully.',
        category="account",
        notification_type="account_connected",
    )

    return OAuthCallbackResponse(
        success=True,
        message="Account connected successfully",
        account_id=result["id"],
        platform=platform,
        account_name=result["account_name"],
    )


# ---------------------------------------------------------
# OAuth Callback
# (LinkedIn, X, Facebook — all share the
# /api/social/callback/{platform} pattern. YouTube's
# callback is defined separately below, on
# youtube_callback_router, since its registered redirect
# URI doesn't match this pattern.)
# ---------------------------------------------------------


@router.get("/callback/{platform}")
def oauth_callback(
    platform: str,
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    platform = platform.lower()

    redis = get_redis()

    user_id = redis.get(f"oauth_state:{state}")

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state",
        )

    redis.delete(f"oauth_state:{state}")

    code_verifier = None

    if platform == "x":

        code_verifier = redis.get(f"oauth_verifier:{state}")

        if not code_verifier:
            raise HTTPException(
                status_code=400,
                detail="Missing or expired PKCE verifier",
            )

        redis.delete(f"oauth_verifier:{state}")

    redirect_uri = REDIRECT_URIS.get(platform)

    service = SocialIntegrationService(db)

    result = service.connect_account(
        platform=platform,
        auth_code=code,
        user_id=int(user_id),
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )

    NotificationService(db).create_notification(
        user_id=int(user_id),
        title="Account Connected",
        description=f'Your {platform} account "{result["account_name"]}" was connected successfully.',
        category="account",
        notification_type="account_connected",
    )

    return {
        "success": True,
        "message": f"{platform} connected successfully",
        "account": result,
        "user_id": int(user_id),
    }


# ---------------------------------------------------------
# YouTube OAuth Callback (separate path)
#
# Registered in Google Cloud Console as:
#   http://localhost:8000/auth/youtube/callback
#
# This lives on youtube_callback_router (no prefix, mounted
# directly in main.py) specifically so the final path is
# exactly /auth/youtube/callback — NOT /api/social/... —
# matching what's already registered there.
# ---------------------------------------------------------


@youtube_callback_router.get("/auth/youtube/callback")
def youtube_oauth_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):

    redis = get_redis()

    user_id = redis.get(f"oauth_state:{state}")

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state",
        )

    redis.delete(f"oauth_state:{state}")

    redirect_uri = REDIRECT_URIS.get("youtube")

    service = SocialIntegrationService(db)

    result = service.connect_account(
        platform="youtube",
        auth_code=code,
        user_id=int(user_id),
        redirect_uri=redirect_uri,
    )

    NotificationService(db).create_notification(
        user_id=int(user_id),
        title="Account Connected",
        description=f'Your youtube account "{result["account_name"]}" was connected successfully.',
        category="account",
        notification_type="account_connected",
    )

    return {
        "success": True,
        "message": "youtube connected successfully",
        "account": result,
        "user_id": int(user_id),
    }


# ---------------------------------------------------------
# Get All Accounts
# ---------------------------------------------------------


@router.get(
    "/accounts",
    response_model=List[SocialAccountResponse],
)
def get_social_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return (
        db.query(SocialAccount)
        .filter(
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .all()
    )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------


@router.get(
    "/accounts/summary",
    response_model=List[SocialAccountSummary],
)
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return (
        db.query(SocialAccount)
        .filter(
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .all()
    )


# ---------------------------------------------------------
# Single Account
# ---------------------------------------------------------


@router.get(
    "/accounts/{account_id}",
    response_model=SocialAccountResponse,
)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    account = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.id == account_id,
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return account


# ---------------------------------------------------------
# Available Platforms
# ---------------------------------------------------------


@router.get(
    "/platforms",
    response_model=List[PlatformInfo],
)
def available_platforms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    platforms = [
        {
            "platform": "facebook",
            "name": "Facebook",
            "icon": "facebook",
        },
        {
            "platform": "instagram",
            "name": "Instagram",
            "icon": "instagram",
        },
        {
            "platform": "linkedin",
            "name": "LinkedIn",
            "icon": "linkedin",
        },
        {
            "platform": "x",
            "name": "X",
            "icon": "x",
        },
        {
            "platform": "youtube",
            "name": "YouTube",
            "icon": "youtube",
        },
    ]

    accounts = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .all()
    )

    result = []

    for platform in platforms:

        account = next(
            (a for a in accounts if a.platform == platform["platform"]),
            None,
        )

        result.append(
            PlatformInfo(
                platform=platform["platform"],
                name=platform["name"],
                icon=platform["icon"],
                is_connected=account is not None,
                account_name=(account.account_name if account else None),
            )
        )

    return result


# ---------------------------------------------------------
# Update Account
# ---------------------------------------------------------


@router.put(
    "/accounts/{account_id}",
    response_model=SocialAccountResponse,
)
def update_account(
    account_id: int,
    update_data: SocialAccountUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    account = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.id == account_id,
            SocialAccount.user_id == current_user.id,
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    for key, value in update_data.dict(exclude_unset=True).items():

        setattr(account, key, value)

    db.commit()
    db.refresh(account)

    return account


# ---------------------------------------------------------
# Disconnect
# ---------------------------------------------------------


@router.delete("/accounts/{account_id}")
def disconnect_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    account = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.id == account_id,
            SocialAccount.user_id == current_user.id,
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    account.is_active = False
    account.is_connected = False

    db.commit()

    NotificationService(db).create_notification(
        user_id=current_user.id,
        title="Account Disconnected",
        description=f"Your {account.platform} account was disconnected.",
        category="account",
        notification_type="account_disconnected",
    )

    return {"message": "Account disconnected successfully"}


# ---------------------------------------------------------
# Refresh Token
# ---------------------------------------------------------


@router.post("/accounts/{account_id}/refresh-token")
def refresh_token(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    account = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.id == account_id,
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    if not account.refresh_token:
        raise HTTPException(
            status_code=400,
            detail="No refresh token available",
        )

    service = SocialIntegrationService(db)

    token = service.refresh_token(
        account.platform,
        account.refresh_token,
    )

    account.access_token = token["access_token"]
    account.token_expires_at = token["expiry"]

    db.commit()

    return {"message": "Token refreshed successfully"}
