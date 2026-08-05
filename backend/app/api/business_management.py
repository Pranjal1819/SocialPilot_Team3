# app/api/business_management.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.business_assignment import BusinessAssignment

router = APIRouter(prefix="/api/business-management", tags=["Business Management"])


# ============================================================
# Get all business users
# ============================================================


@router.get("/business-users")
def get_business_users(db: Session = Depends(get_db)):

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
# Get single business user
# ============================================================


@router.get("/business-users/{user_id}")
def get_business_user(user_id: int, db: Session = Depends(get_db)):

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
# ============================================================


@router.get("/marketing-team/{marketing_team_id}/businesses")
def get_assigned_businesses(marketing_team_id: int, db: Session = Depends(get_db)):

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
# Get marketing teams
# ============================================================


@router.get("/marketing-teams")
def get_marketing_teams(db: Session = Depends(get_db)):

    teams = db.query(User).filter(User.role == "marketing_team").all()

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
