# app/api/business_management.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user
from app.models.user import User
from app.models.business_assignment import BusinessAssignment

router = APIRouter(prefix="/api/business-management", tags=["Business Management"])


# ============================================================
# Get all business users (Admin only)
# ============================================================


@router.get("/business-users")
def get_business_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    users = db.query(User).filter(User.role == "business_user").all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "profile_picture": user.profile_picture,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
        for user in users
    ]


# ============================================================
# Get single business user (Admin only)
# ============================================================


@router.get("/business-users/{user_id}")
def get_business_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    user = (
        db.query(User).filter(User.id == user_id, User.role == "business_user").first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Business user not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "profile_picture": user.profile_picture,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


# ============================================================
# Get businesses assigned to marketing team
# (Admin, or the marketing team itself)
# ============================================================


@router.get("/marketing-team/{marketing_team_id}/businesses")
def get_assigned_businesses(
    marketing_team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Only the marketing team itself or an administrator may view
    # the businesses assigned to a given marketing team.
    if current_user.role != "administrator" and current_user.id != marketing_team_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view these businesses",
        )

    assignments = (
        db.query(BusinessAssignment)
        .filter(BusinessAssignment.marketing_team_id == marketing_team_id)
        .all()
    )

    businesses = []

    for assignment in assignments:

        business = db.query(User).filter(User.id == assignment.business_user_id).first()

        if business:
            businesses.append(
                {
                    "id": business.id,
                    "name": business.name,
                    "email": business.email,
                    "role": business.role,
                }
            )

    return {"marketing_team_id": marketing_team_id, "businesses": businesses}


# ============================================================
# Get marketing teams (Admin and business users)
# ============================================================


@router.get("/marketing-teams")
def get_marketing_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.role not in {"administrator", "business_user"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view marketing teams",
        )

    teams = (
        db.query(User)
        .filter(User.role == "marketing_team", User.is_active.is_(True))
        .all()
    )

    return [
        {
            "id": team.id,
            "name": team.name,
            "email": team.email,
            "role": team.role,
            "profile_picture": team.profile_picture,
            "is_active": team.is_active,
            "created_at": team.created_at,
        }
        for team in teams
    ]