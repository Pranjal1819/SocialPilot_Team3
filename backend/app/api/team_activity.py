from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.campaign import Campaign

from app.schemas.team_activity import TeamActivityItem

router = APIRouter(prefix="/api/team-activity", tags=["Team Activity"])


@router.get("/", response_model=List[TeamActivityItem])
def get_team_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    campaigns = (
        db.query(Campaign)
        .filter(
            (Campaign.user_id == current_user.id)
            | (Campaign.marketing_team_id == current_user.id)
        )
        .all()
    )

    activity: List[TeamActivityItem] = []

    for campaign in campaigns:

        assigned_to = campaign.marketing_team.name if campaign.marketing_team else None

        if campaign.marketing_team_id:

            activity.append(
                TeamActivityItem(
                    id=f"campaign_assigned_{campaign.id}",
                    type="campaign_assigned",
                    title="Campaign Assigned",
                    description=f'"{campaign.name}" was assigned to {assigned_to}.',
                    campaign_name=campaign.name,
                    user_name=assigned_to or "Unknown",
                    timestamp=campaign.created_at,
                )
            )

        if campaign.updated_at and campaign.updated_at != campaign.created_at:

            activity.append(
                TeamActivityItem(
                    id=f"campaign_updated_{campaign.id}",
                    type="campaign_updated",
                    title="Campaign Updated",
                    description=f'"{campaign.name}" was updated.',
                    campaign_name=campaign.name,
                    user_name=campaign.user.name if campaign.user else "Unknown",
                    timestamp=campaign.updated_at,
                )
            )

    activity.sort(key=lambda item: item.timestamp, reverse=True)

    return activity
