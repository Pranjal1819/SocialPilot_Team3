from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.business_assignment import BusinessAssignment

router = APIRouter(prefix="/api/business", tags=["Business Management"])


# =====================================================
# Assign Business User to Marketing Team
# =====================================================


@router.post("/assign")
def assign_business_to_marketing(
    business_user_id: int,
    marketing_team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Only admin can assign

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403, detail="Only administrator can assign businesses"
        )

    business_user = (
        db.query(User)
        .filter(User.id == business_user_id, User.role == "business_user")
        .first()
    )

    if not business_user:

        raise HTTPException(status_code=404, detail="Business user not found")

    marketing_team = (
        db.query(User)
        .filter(User.id == marketing_team_id, User.role == "marketing_team")
        .first()
    )

    if not marketing_team:

        raise HTTPException(status_code=404, detail="Marketing team not found")

    # Check duplicate assignment

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
            status_code=400, detail="Business already assigned to this marketing team"
        )

    assignment = BusinessAssignment(
        business_user_id=business_user_id, marketing_team_id=marketing_team_id
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
# Marketing Team Dashboard
# Get only assigned businesses
# =====================================================


@router.get("/my-clients")
def get_my_business_clients(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    if current_user.role != "marketing_team":

        raise HTTPException(
            status_code=403, detail="Only marketing team can access clients"
        )

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
                    "role": business.role,
                }
            )

    return clients


# =====================================================
# Business User Dashboard
# View assigned Marketing Team
# =====================================================


@router.get("/my-marketing-team")
def get_my_marketing_team(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    if current_user.role != "business_user":

        raise HTTPException(
            status_code=403, detail="Only business users can access this"
        )

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
                    "role": team.role,
                }
            )

    return teams
