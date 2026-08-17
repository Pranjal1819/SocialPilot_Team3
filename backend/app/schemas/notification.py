from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationResponse(BaseModel):

    id: int
    user_id: int
    title: Optional[str] = None
    message: str
    category: Optional[str] = None
    type: str
    delivery_channel: str
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):

    total: int
    skip: int
    limit: int
    notifications: list[NotificationResponse]


class NotificationPreferenceResponse(BaseModel):

    id: int
    user_id: int
    publishing_enabled: bool
    campaign_enabled: bool
    account_activity_enabled: bool
    team_collaboration_enabled: bool
    system_enabled: bool
    in_app_enabled: bool
    email_enabled: bool
    push_enabled: bool
    email_frequency: str
    promotional_emails_enabled: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationPreferenceUpdate(BaseModel):

    publishing_enabled: Optional[bool] = None
    campaign_enabled: Optional[bool] = None
    account_activity_enabled: Optional[bool] = None
    team_collaboration_enabled: Optional[bool] = None
    system_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None


class EmailPreferenceUpdate(BaseModel):

    email_frequency: Optional[str] = None
    promotional_emails_enabled: Optional[bool] = None
