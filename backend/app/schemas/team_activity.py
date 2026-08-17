from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TeamActivityItem(BaseModel):
    id: str
    type: str
    title: str
    description: str
    campaign_name: Optional[str] = None
    user_name: str
    timestamp: datetime

    class Config:
        from_attributes = True