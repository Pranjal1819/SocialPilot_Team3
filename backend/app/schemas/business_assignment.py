from pydantic import BaseModel
from datetime import datetime


class BusinessAssignmentCreate(BaseModel):

    business_user_id: int

    marketing_team_id: int


class BusinessAssignmentResponse(BaseModel):

    id: int

    business_user_id: int

    marketing_team_id: int

    assigned_at: datetime

    class Config:
        from_attributes = True
