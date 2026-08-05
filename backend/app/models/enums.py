from enum import Enum


class UserRole(str, Enum):
    ADMIN = "administrator"
    BUSINESS_USER = "business_user"
    MARKETING_TEAM = "marketing_team"
    CONTENT_CREATOR = "content_creator"
