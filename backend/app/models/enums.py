from enum import Enum


class UserRole(str, Enum):
    ADMIN = "administrator"
    BUSINESS_USER = "business_user"
    MARKETING_TEAM = "marketing_team"
    CONTENT_CREATOR = "content_creator"


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    REEL = "reel"
    AUDIO = "audio"
    DOCUMENT = "document"


# content_type values that require at least one PostMedia row
MEDIA_REQUIRED_CONTENT_TYPES = {
    ContentType.IMAGE,
    ContentType.VIDEO,
    ContentType.CAROUSEL,
    ContentType.STORY,
    ContentType.REEL,
    ContentType.AUDIO,
    ContentType.DOCUMENT,
}
