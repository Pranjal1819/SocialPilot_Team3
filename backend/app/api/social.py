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

router = APIRouter(
    prefix="/api/social",
    tags=["Social Accounts"],
)

LINKEDIN_REDIRECT_URI = "http://localhost:8000/api/social/callback/linkedin"

SUPPORTED_PLATFORMS = [
    "linkedin",
    "facebook",
    "instagram",
    "twitter",
    "youtube",
]


# ---------------------------------------------------------
# Generate OAuth URL
# ---------------------------------------------------------


@router.get("/auth-url/{platform}", response_model=OAuthURLResponse)
def get_oauth_url(
    platform: str,
    redirect_uri: str = LINKEDIN_REDIRECT_URI,
    current_user: User = Depends(get_current_user),
):

    if platform.lower() not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported platform",
        )

    service = SocialIntegrationService(None)

    auth_url = service.get_oauth_url(
        platform=platform,
        redirect_uri=redirect_uri,
    )

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

    service = SocialIntegrationService(db)

    result = service.connect_account(
        platform=connect_data.platform,
        auth_code=connect_data.auth_code,
        user_id=current_user.id,
        redirect_uri=connect_data.redirect_uri or LINKEDIN_REDIRECT_URI,
    )

    return OAuthCallbackResponse(
        success=True,
        message="Account connected successfully",
        account_id=result["id"],
        platform=connect_data.platform,
        account_name=result["account_name"],
    )


# ---------------------------------------------------------
# OAuth Callback
# ---------------------------------------------------------


@router.get("/callback/{platform}")
def oauth_callback(
    platform: str,
    code: str,
    db: Session = Depends(get_db),
):

    service = SocialIntegrationService(db)

    # Temporary user
    # Replace later using OAuth state/session

    result = service.connect_account(
        platform=platform,
        auth_code=code,
        user_id=1,
        redirect_uri=LINKEDIN_REDIRECT_URI,
    )

    return {
        "success": True,
        "message": f"{platform} connected successfully",
        "account": result,
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
            "platform": "twitter",
            "name": "Twitter/X",
            "icon": "twitter",
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
