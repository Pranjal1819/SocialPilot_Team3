# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import requests
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ==================== LinkedIn OAuth ====================

@router.get("/linkedin/login")
def linkedin_login(
    redirect_uri: Optional[str] = None
):
    """
    Step 1: Redirect ANY user to LinkedIn for authentication
    """
    frontend_redirect = redirect_uri or settings.LINKEDIN_REDIRECT_URI_FRONTEND
    
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": "openid profile email",
        "state": frontend_redirect
    }

    linkedin_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        + urlencode(params)
    )

    return RedirectResponse(url=linkedin_url)


@router.get("/linkedin/callback")
def linkedin_callback(
    code: Optional[str] = None,
    error: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Step 2: Handle LinkedIn callback for ANY user
    Handles 3 cases:
    1. Existing user with LinkedIn ID
    2. Existing user with same email (update with LinkedIn ID)
    3. Brand new user (create account)
    """
    
    frontend_url = state or settings.LINKEDIN_REDIRECT_URI_FRONTEND
    
    # Handle errors
    if error:
        return RedirectResponse(
            url=f"{frontend_url}?error={error}"
        )
    
    if not code:
        return RedirectResponse(
            url=f"{frontend_url}?error=missing_code"
        )

    try:
        # Exchange code for access token
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            return RedirectResponse(
                url=f"{frontend_url}?error=no_access_token"
            )

        # Get user info from LinkedIn
        user_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if user_response.status_code != 200:
            return RedirectResponse(
                url=f"{frontend_url}?error=userinfo_fetch_failed"
            )
            
        user_data = user_response.json()

        linkedin_id = user_data.get("sub")  # Unique LinkedIn ID
        email = user_data.get("email")
        name = user_data.get("name")
        picture = user_data.get("picture")

        if not linkedin_id or not email:
            return RedirectResponse(
                url=f"{frontend_url}?error=missing_user_data"
            )

        # ================================================================
        # ✅ CASE 1: User already connected via LinkedIn before
        # ================================================================
        existing_user = db.query(User).filter(
            User.linkedin_id == linkedin_id
        ).first()

        if existing_user:
            user = existing_user
            print(f"✅ Existing user found: {user.email} (LinkedIn ID: {linkedin_id})")
        
        else:
            # ============================================================
            # ✅ CASE 2: User exists with same email but no LinkedIn ID
            # ============================================================
            email_user = db.query(User).filter(User.email == email).first()
            
            if email_user:
                # Update existing user with LinkedIn ID
                email_user.linkedin_id = linkedin_id
                if picture:
                    email_user.profile_picture = picture
                db.commit()
                db.refresh(email_user)
                user = email_user
                print(f"✅ Updated existing user: {user.email} with LinkedIn ID: {linkedin_id}")
            
            else:
                # ==========================================================
                # ✅ CASE 3: Brand new user - Create account
                # ==========================================================
                new_user = User(
                    email=email,
                    name=name,
                    linkedin_id=linkedin_id,
                    profile_picture=picture,
                    password=None,  # No password for OAuth users
                    role="user",
                    is_active=True
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user = new_user
                print(f"✅ Created new user: {user.email} with LinkedIn ID: {linkedin_id}")

        # ================================================================
        # ✅ Generate JWT token for ANY user (Works for everyone)
        # ================================================================
        jwt_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        # ================================================================
        # ✅ Redirect to frontend with token (Works for ANY user)
        # ================================================================
        redirect_url = f"{frontend_url}?token={jwt_token}&user_id={user.id}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        print(f"❌ LinkedIn callback error: {str(e)}")
        return RedirectResponse(
            url=f"{frontend_url}?error={str(e)}"
        )


# ==================== Email/Password Authentication ====================

@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user with email and password"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = User(
        email=user.email,
        name=user.name,
        password=get_password_hash(user.password),
        role="user",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not user.password or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user"""
    return current_user


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
):
    """Logout user"""
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """Refresh JWT token"""
    new_token = create_access_token(
        data={"sub": current_user.email, "user_id": current_user.id}
    )
    return {"access_token": new_token, "token_type": "bearer"}