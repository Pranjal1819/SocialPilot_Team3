from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ==========================================================
# Current Logged-in User
# ==========================================================


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return user


# ==========================================================
# Administrator Only
# ==========================================================


def get_current_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )

    return current_user


# ==========================================================
# Business User Only
# ==========================================================


def get_current_business_user(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "business_user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business User access required",
        )

    return current_user


# ==========================================================
# Marketing Team Only
# ==========================================================


def get_current_marketing_team(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "marketing_team":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Marketing Team access required",
        )

    return current_user


# ==========================================================
# Content Creator Only
# ==========================================================


def get_current_content_creator(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "content_creator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content Creator access required",
        )

    return current_user


# ==========================================================
# Marketing Team OR Admin
# ==========================================================


def get_marketing_or_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["marketing_team", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Marketing Team or Administrator access required",
        )

    return current_user


# ==========================================================
# Business User OR Admin
# ==========================================================


def get_business_or_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["business_user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business User or Administrator access required",
        )

    return current_user
