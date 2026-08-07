# app/api/business_assignment.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.role_checker import require_roles

from app.models.user import User
from app.models.business_assignment import BusinessAssignment

router = APIRouter(
    prefix="/api/business",
    tags=["Business Assignment"],
)


# =====================================================
# Assign Business User to Marketing Team
# Admin Only
# =====================================================


@router.post("/assign")
def assign_business_to_marketing(
    business_user_id: int,
    marketing_team_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_roles("admin")),
):

    business_user = (
        db.query(User)
        .filter(
            User.id == business_user_id,
            User.role == "business_user",
        )
        .first()
    )

    if not business_user:
        raise HTTPException(
            status_code=404,
            detail="Business user not found",
        )

    marketing_team = (
        db.query(User)
        .filter(
            User.id == marketing_team_id,
            User.role == "marketing_team",
        )
        .first()
    )

    if not marketing_team:
        raise HTTPException(
            status_code=404,
            detail="Marketing team not found",
        )

    existing = (
        db.query(BusinessAssignment)
        .filter(
            BusinessAssignment.business_user_id == business_user_id,
            BusinessAssignment.marketing_team_id == marketing_team_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Business already assigned to this marketing team",
        )

    assignment = BusinessAssignment(
        business_user_id=business_user_id,
        marketing_team_id=marketing_team_id,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {
        "message": "Business assigned successfully",
        "assignment_id": assignment.id,
        "business_user": business_user.name,
        "marketing_team": marketing_team.name,
    }


# =====================================================
# Admin - View All Assignments
# =====================================================


@router.get("/assignments")
def get_all_assignments(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_roles("admin")),
):

    assignments = db.query(BusinessAssignment).all()

    result = []

    for assignment in assignments:

        business = db.query(User).filter(User.id == assignment.business_user_id).first()

        team = db.query(User).filter(User.id == assignment.marketing_team_id).first()

        result.append(
            {
                "assignment_id": assignment.id,
                "business_user": {
                    "id": business.id,
                    "name": business.name,
                    "email": business.email,
                },
                "marketing_team": {
                    "id": team.id,
                    "name": team.name,
                    "email": team.email,
                },
                "assigned_at": assignment.assigned_at,
            }
        )

    return result


# =====================================================
# Admin - Remove Assignment
# =====================================================


@router.delete("/assign/{assignment_id}")
def remove_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_roles("admin")),
):

    assignment = (
        db.query(BusinessAssignment)
        .filter(BusinessAssignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found",
        )

    db.delete(assignment)
    db.commit()

    return {"message": "Assignment removed successfully"}


# =====================================================
# Marketing Team Dashboard
# View Assigned Business Users
# =====================================================


@router.get("/my-clients")
def get_my_business_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("marketing_team")),
):

    assignments = (
        db.query(BusinessAssignment)
        .filter(BusinessAssignment.marketing_team_id == current_user.id)
        .all()
    )

    clients = []

    for assignment in assignments:

        business = db.query(User).filter(User.id == assignment.business_user_id).first()

        if business:

            clients.append(
                {
                    "id": business.id,
                    "name": business.name,
                    "email": business.email,
                    "organization": business.organization,
                    "role": business.role,
                }
            )

    return clients


# =====================================================
# Business User Dashboard
# View Assigned Marketing Teams
# =====================================================


@router.get("/my-marketing-team")
def get_my_marketing_team(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("business_user")),
):

    assignments = (
        db.query(BusinessAssignment)
        .filter(BusinessAssignment.business_user_id == current_user.id)
        .all()
    )

    teams = []

    for assignment in assignments:

        team = db.query(User).filter(User.id == assignment.marketing_team_id).first()

        if team:

            teams.append(
                {
                    "id": team.id,
                    "name": team.name,
                    "email": team.email,
                    "organization": team.organization,
                    "role": team.role,
                }
            )

    return teams
