import secrets

from app.core.config import settings
from app.services.redis_client import get_redis

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

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


# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/api/social",
    tags=["Social Accounts"],
)


# =========================================================
# Separate OAuth Callback Routers
#
# YouTube:
# /auth/youtube/callback
#
# Instagram:
# /auth/instagram/callback
# =========================================================

youtube_callback_router = APIRouter(
    tags=["Social Accounts"]
)

instagram_callback_router = APIRouter(
    tags=["Social Accounts"]
)


# =========================================================
# Redirect URIs
# =========================================================

REDIRECT_URIS = {
    "linkedin": "http://localhost:8000/api/social/callback/linkedin",

    # Existing routes — DO NOT CHANGE
    "x": "http://localhost:8000/api/social/callback/x",
    "facebook": "http://localhost:8000/api/social/callback/facebook",

    # Existing YouTube URI
    "youtube": settings.YOUTUBE_REDIRECT_URI,

    # Instagram ngrok URI from .env
    "instagram": settings.INSTAGRAM_REDIRECT_URI,
}


# =========================================================
# Supported Platforms
# =========================================================

SUPPORTED_PLATFORMS = [
    "linkedin",
    "facebook",
    "instagram",
    "x",
    "youtube",
]


# =========================================================
# Frontend Redirect Configuration
# =========================================================

FRONTEND_BASE_URL = "http://localhost:3000"

ROLE_ACCOUNTS_PATH = {
    "content_creator": "/content-creator/accounts",
    "business_user": "/business-owner/accounts",
}


def get_accounts_redirect(
    role: str,
    error: str = None,
    platform: str = None,
):
    """
    Redirect the user back to the appropriate SocialPilot
    accounts page after OAuth completion.
    """

    path = ROLE_ACCOUNTS_PATH.get(
        role,
        "/content-creator/accounts",
    )

    url = f"{FRONTEND_BASE_URL}{path}"

    if error:
        separator = "?" if "?" not in url else "&"

        url += (
            f"{separator}"
            f"error={error}"
            f"&platform={platform}"
        )

    # IMPORTANT:
    # Always return RedirectResponse, including
    # successful OAuth completion.
    return RedirectResponse(
        url=url,
        status_code=302,
    )


# =========================================================
# Generate OAuth URL
# =========================================================

@router.get(
    "/auth-url/{platform}",
    response_model=OAuthURLResponse,
)
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

    # -----------------------------------------------------
    # Generate OAuth state
    # -----------------------------------------------------

    state = secrets.token_urlsafe(32)

    redis = get_redis()

    redis.setex(
        f"oauth_state:{state}",
        600,
        str(current_user.id),
    )

    # -----------------------------------------------------
    # X PKCE
    # -----------------------------------------------------

    code_challenge = None

    if platform == "x":

        x_service = XService()

        code_verifier, code_challenge = (
            x_service.generate_pkce_pair()
        )

        redis.setex(
            f"oauth_verifier:{state}",
            600,
            code_verifier,
        )

    # -----------------------------------------------------
    # Generate OAuth URL
    # -----------------------------------------------------

    auth_url = service.get_oauth_url(
        platform=platform,
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
    )

    # X service already handles state.
    # Other platforms need state appended here.

    if platform != "x":

        separator = (
            "&"
            if "?" in auth_url
            else "?"
        )

        auth_url = (
            f"{auth_url}"
            f"{separator}"
            f"state={state}"
        )

    return OAuthURLResponse(
        platform=platform,
        auth_url=auth_url,
        redirect_uri=redirect_uri,
    )


# =========================================================
# Connect Account
#
# Manual/API-based connection endpoint.
# =========================================================

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

    redirect_uri = (
        connect_data.redirect_uri
        or REDIRECT_URIS.get(platform)
    )

    service = SocialIntegrationService(db)

    result = service.connect_account(
        platform=platform,
        auth_code=connect_data.auth_code,
        user_id=current_user.id,
        redirect_uri=redirect_uri,
        code_verifier=getattr(
            connect_data,
            "code_verifier",
            None,
        ),
    )

    NotificationService(db).create_notification(
        user_id=current_user.id,
        title="Account Connected",
        description=(
            f'Your {platform} account '
            f'"{result["account_name"]}" '
            f'was connected successfully.'
        ),
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


# =========================================================
# Generic OAuth Callback
#
# LinkedIn
# X
# Facebook
#
# LinkedIn redirects to SocialPilot frontend.
# X/Facebook retain JSON behavior for now.
# =========================================================

@router.get(
    "/callback/{platform}"
)
def oauth_callback(
    platform: str,
    code: str,
    state: str,
    db: Session = Depends(get_db),
):

    platform = platform.lower()

    redis = get_redis()

    # -----------------------------------------------------
    # Validate OAuth state
    # -----------------------------------------------------

    user_id = redis.get(
        f"oauth_state:{state}"
    )

    if not user_id:

        if platform == "linkedin":

            return get_accounts_redirect(
                "content_creator",
                error="invalid_state",
                platform=platform,
            )

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state",
        )

    redis.delete(
        f"oauth_state:{state}"
    )

    # -----------------------------------------------------
    # Get user
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    role = (
        user.role
        if user
        else "content_creator"
    )

    # -----------------------------------------------------
    # X PKCE
    # -----------------------------------------------------

    code_verifier = None

    if platform == "x":

        code_verifier = redis.get(
            f"oauth_verifier:{state}"
        )

        if not code_verifier:

            raise HTTPException(
                status_code=400,
                detail="Missing or expired PKCE verifier",
            )

        redis.delete(
            f"oauth_verifier:{state}"
        )

    # -----------------------------------------------------
    # Redirect URI
    # -----------------------------------------------------

    redirect_uri = REDIRECT_URIS.get(
        platform
    )

    if not redirect_uri:

        if platform == "linkedin":

            return get_accounts_redirect(
                role,
                error="missing_redirect_uri",
                platform=platform,
            )

        raise HTTPException(
            status_code=400,
            detail=(
                f"No redirect URI configured "
                f"for {platform}"
            ),
        )

    service = SocialIntegrationService(db)

    # -----------------------------------------------------
    # Connect Account
    # -----------------------------------------------------

    try:

        result = service.connect_account(
            platform=platform,
            auth_code=code,
            user_id=int(user_id),
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )

    except Exception as e:

        print(
            f"{platform} OAuth connection failed:",
            e,
        )

        if platform == "linkedin":

            return get_accounts_redirect(
                role,
                error="connection_failed",
                platform=platform,
            )

        raise HTTPException(
            status_code=400,
            detail=f"{platform} connection failed",
        )

    # -----------------------------------------------------
    # Notification
    # -----------------------------------------------------

    NotificationService(db).create_notification(
        user_id=int(user_id),
        title="Account Connected",
        description=(
            f'Your {platform} account '
            f'"{result["account_name"]}" '
            f'was connected successfully.'
        ),
        category="account",
        notification_type="account_connected",
    )

    # -----------------------------------------------------
    # LinkedIn → SocialPilot frontend
    # -----------------------------------------------------

    if platform == "linkedin":

        return get_accounts_redirect(
            role
        )

    # -----------------------------------------------------
    # X / Facebook
    #
    # Existing JSON response preserved.
    # -----------------------------------------------------

    return {
        "success": True,
        "message": (
            f"{platform} connected successfully"
        ),
        "account": result,
        "user_id": int(user_id),
    }


# =========================================================
# YouTube OAuth Callback
#
# Existing registered URI:
#
# http://localhost:8000/auth/youtube/callback
#
# Flow:
#
# YouTube
#    ↓
# FastAPI
#    ↓
# SocialPilot frontend
# =========================================================

@youtube_callback_router.get(
    "/auth/youtube/callback"
)
def youtube_oauth_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):

    redis = get_redis()

    # -----------------------------------------------------
    # Validate state
    # -----------------------------------------------------

    user_id = redis.get(
        f"oauth_state:{state}"
    )

    if not user_id:

        return get_accounts_redirect(
            "content_creator",
            error="invalid_state",
            platform="youtube",
        )

    redis.delete(
        f"oauth_state:{state}"
    )

    # -----------------------------------------------------
    # Get user
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    role = (
        user.role
        if user
        else "content_creator"
    )

    # -----------------------------------------------------
    # Redirect URI
    # -----------------------------------------------------

    redirect_uri = REDIRECT_URIS.get(
        "youtube"
    )

    if not redirect_uri:

        return get_accounts_redirect(
            role,
            error="missing_redirect_uri",
            platform="youtube",
        )

    service = SocialIntegrationService(db)

    # -----------------------------------------------------
    # Connect YouTube Account
    # -----------------------------------------------------

    try:

        result = service.connect_account(
            platform="youtube",
            auth_code=code,
            user_id=int(user_id),
            redirect_uri=redirect_uri,
        )

    except Exception as e:

        print(
            "YouTube OAuth connection failed:",
            e,
        )

        return get_accounts_redirect(
            role,
            error="connection_failed",
            platform="youtube",
        )

    # -----------------------------------------------------
    # Notification
    # -----------------------------------------------------

    NotificationService(db).create_notification(
        user_id=int(user_id),
        title="Account Connected",
        description=(
            f'Your YouTube account '
            f'"{result["account_name"]}" '
            f'was connected successfully.'
        ),
        category="account",
        notification_type="account_connected",
    )

    # -----------------------------------------------------
    # Redirect to SocialPilot
    # -----------------------------------------------------

    return get_accounts_redirect(
        role
    )


# =========================================================
# Instagram OAuth Callback
#
# Registered URI:
#
# https://<your-ngrok-domain>/auth/instagram/callback
#
# Flow:
#
# Instagram
#    ↓
# ngrok
#    ↓
# FastAPI
#    ↓
# SocialPilot frontend
# =========================================================

@instagram_callback_router.get(
    "/auth/instagram/callback"
)
def instagram_oauth_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):

    redis = get_redis()

    # -----------------------------------------------------
    # Validate OAuth state
    # -----------------------------------------------------

    user_id = redis.get(
        f"oauth_state:{state}"
    )

    if not user_id:

        return get_accounts_redirect(
            "content_creator",
            error="invalid_state",
            platform="instagram",
        )

    redis.delete(
        f"oauth_state:{state}"
    )

    # -----------------------------------------------------
    # Get user
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    role = (
        user.role
        if user
        else "content_creator"
    )

    # -----------------------------------------------------
    # Instagram Redirect URI
    # -----------------------------------------------------

    redirect_uri = REDIRECT_URIS.get(
        "instagram"
    )

    if not redirect_uri:

        return get_accounts_redirect(
            role,
            error="missing_redirect_uri",
            platform="instagram",
        )

    service = SocialIntegrationService(db)

    # -----------------------------------------------------
    # Connect Instagram Account
    # -----------------------------------------------------

    try:

        result = service.connect_account(
            platform="instagram",
            auth_code=code,
            user_id=int(user_id),
            redirect_uri=redirect_uri,
        )

    except Exception as e:

        print(
            "Instagram OAuth connection failed:",
            e,
        )

        return get_accounts_redirect(
            role,
            error="connection_failed",
            platform="instagram",
        )

    # -----------------------------------------------------
    # Notification
    # -----------------------------------------------------

    NotificationService(db).create_notification(
        user_id=int(user_id),
        title="Account Connected",
        description=(
            f'Your Instagram account '
            f'"{result["account_name"]}" '
            f'was connected successfully.'
        ),
        category="account",
        notification_type="account_connected",
    )

    # -----------------------------------------------------
    # Redirect to SocialPilot
    # -----------------------------------------------------

    return get_accounts_redirect(
        role
    )


# =========================================================
# Get All Accounts
# =========================================================

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


# =========================================================
# Summary
# =========================================================

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


# =========================================================
# Single Account
# =========================================================

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


# =========================================================
# Available Platforms
# =========================================================

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
            (
                a
                for a in accounts
                if a.platform == platform["platform"]
            ),
            None,
        )

        result.append(
            PlatformInfo(
                platform=platform["platform"],
                name=platform["name"],
                icon=platform["icon"],
                is_connected=account is not None,
                account_name=(
                    account.account_name
                    if account
                    else None
                ),
            )
        )

    return result


# =========================================================
# Update Account
# =========================================================

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

    for key, value in update_data.dict(
        exclude_unset=True
    ).items():

        setattr(
            account,
            key,
            value,
        )

    db.commit()
    db.refresh(account)

    return account


# =========================================================
# Disconnect
# =========================================================

@router.delete(
    "/accounts/{account_id}"
)
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
        description=(
            f"Your {account.platform} account "
            f"was disconnected."
        ),
        category="account",
        notification_type="account_disconnected",
    )

    return {
        "message": "Account disconnected successfully"
    }


# =========================================================
# Refresh Token
# =========================================================

@router.post(
    "/accounts/{account_id}/refresh-token"
)
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

    return {
        "message": "Token refreshed successfully"
    }