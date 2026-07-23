from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.social_account import SocialAccount
from app.schemas.social_account import (
    SocialAccountCreate,
    SocialAccountUpdate,
    SocialAccountResponse,
    SocialAccountConnect,
    OAuthURLResponse,
    OAuthCallbackResponse,
    PlatformInfo,
    SocialAccountSummary
)
from app.services.social_integration import SocialIntegrationService

router = APIRouter(prefix="/api/social", tags=["Social Accounts"])

@router.get("/auth-url/{platform}", response_model=OAuthURLResponse)
def get_oauth_url(
    platform: str,
    redirect_uri: str,
    current_user: User = Depends(get_current_user)
):
    """Get OAuth URL for connecting a social media platform"""
    service = SocialIntegrationService(None)
    auth_url = service.get_oauth_url(platform, redirect_uri)
    
    return OAuthURLResponse(
        platform=platform,
        auth_url=auth_url,
        redirect_uri=redirect_uri
    )

@router.post("/connect", response_model=OAuthCallbackResponse)
def connect_social_account(
    connect_data: SocialAccountConnect,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect a social media account using OAuth code"""
    service = SocialIntegrationService(db)
    
    try:
        result = service.connect_account(
            platform=connect_data.platform,
            auth_code=connect_data.auth_code,
            user_id=current_user.id
        )
        
        return OAuthCallbackResponse(
            success=True,
            message=f"Successfully connected {connect_data.platform}",
            account_id=result.get("id"),
            platform=connect_data.platform,
            account_name=result.get("account_name")
        )
    except Exception as e:
        return OAuthCallbackResponse(
            success=False,
            message=str(e)
        )

@router.get("/accounts", response_model=List[SocialAccountResponse])
def get_social_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all social accounts for the current user"""
    accounts = db.query(SocialAccount).filter(
        SocialAccount.user_id == current_user.id,
        SocialAccount.is_active == True
    ).all()
    
    return accounts

@router.get("/accounts/summary", response_model=List[SocialAccountSummary])
def get_social_accounts_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get simplified social accounts list"""
    accounts = db.query(SocialAccount).filter(
        SocialAccount.user_id == current_user.id,
        SocialAccount.is_active == True
    ).all()
    
    return accounts

@router.get("/platforms", response_model=List[PlatformInfo])
def get_available_platforms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of supported platforms with connection status"""
    platforms = [
        {"platform": "facebook", "name": "Facebook", "icon": "fb"},
        {"platform": "instagram", "name": "Instagram", "icon": "ig"},
        {"platform": "linkedin", "name": "LinkedIn", "icon": "li"},
        {"platform": "twitter", "name": "Twitter/X", "icon": "tw"},
        {"platform": "youtube", "name": "YouTube", "icon": "yt"},
        {"platform": "pinterest", "name": "Pinterest", "icon": "pin"}
    ]
    
    # Check which platforms are connected
    connected_accounts = db.query(SocialAccount).filter(
        SocialAccount.user_id == current_user.id,
        SocialAccount.is_active == True
    ).all()
    
    connected_platforms = [acc.platform for acc in connected_accounts]
    
    result = []
    for platform in platforms:
        result.append(PlatformInfo(
            platform=platform["platform"],
            name=platform["name"],
            icon=platform["icon"],
            is_connected=platform["platform"] in connected_platforms,
            account_name=next(
                (acc.account_name for acc in connected_accounts 
                 if acc.platform == platform["platform"]), 
                None
            )
        ))
    
    return result

@router.put("/accounts/{account_id}", response_model=SocialAccountResponse)
def update_social_account(
    account_id: int,
    update_data: SocialAccountUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a social account"""
    account = db.query(SocialAccount).filter(
        SocialAccount.id == account_id,
        SocialAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(account, key, value)
    
    db.commit()
    db.refresh(account)
    return account

@router.delete("/accounts/{account_id}")
def disconnect_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect a social account"""
    account = db.query(SocialAccount).filter(
        SocialAccount.id == account_id,
        SocialAccount.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.is_active = False
    db.commit()
    
    return {"message": f"Account {account.account_name} disconnected successfully"}

@router.post("/accounts/{account_id}/refresh-token")
def refresh_access_token(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Refresh the access token for a social account"""
    account = db.query(SocialAccount).filter(
        SocialAccount.id == account_id,
        SocialAccount.user_id == current_user.id,
        SocialAccount.is_active == True
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if not account.refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token available")
    
    service = SocialIntegrationService(db)
    new_token = service.refresh_token(account.platform, account.refresh_token)
    
    account.access_token = new_token.get("access_token")
    account.token_expiry = new_token.get("expiry")
    db.commit()
    
    return {"message": "Token refreshed successfully"}