from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.social_account import SocialAccount
from app.services.social.linkedin import LinkedInService
from app.core.security import encrypt_token


class SocialIntegrationService:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------
    # Get Platform Service
    # --------------------------------------------------

    def get_platform_service(self, platform: str):

        platform = platform.lower()

        if platform == "linkedin":
            return LinkedInService()

        raise Exception(f"Unsupported platform: {platform}")

    # --------------------------------------------------
    # Generate OAuth URL
    # --------------------------------------------------

    def get_oauth_url(
        self,
        platform: str,
        redirect_uri: str,
    ):

        service = self.get_platform_service(platform)

        return service.get_oauth_url(redirect_uri)

    # --------------------------------------------------
    # Connect Social Account
    # --------------------------------------------------

    def connect_account(
        self,
        platform: str,
        auth_code: str,
        user_id: int,
        redirect_uri: str,
    ):

        service = self.get_platform_service(platform)

        # ---------------------------------------
        # Exchange OAuth Code
        # ---------------------------------------

        token_data = service.exchange_code(
            auth_code,
            redirect_uri,
        )

        access_token = token_data.get("access_token")

        refresh_token = token_data.get("refresh_token")

        expires_in = token_data.get("expires_in")

        if not access_token:
            raise Exception("Failed to obtain access token")

        # ---------------------------------------
        # Fetch User Profile
        # ---------------------------------------

        profile = service.get_profile(access_token)

        account_name = (
            profile.get("name") or profile.get("localizedFirstName") or "LinkedIn User"
        )

        account_id = profile.get("sub") or profile.get("id")

        # ---------------------------------------
        # Prevent Duplicate Connection
        # Same LinkedIn account
        # ---------------------------------------

        existing = (
            self.db.query(SocialAccount)
            .filter(
                SocialAccount.user_id == user_id,
                SocialAccount.platform == platform,
                SocialAccount.account_id == account_id,
            )
            .first()
        )

        expiry = None

        if expires_in:
            expiry = datetime.utcnow() + timedelta(seconds=expires_in)

        if existing:

            existing.account_name = account_name
            existing.access_token = encrypt_token(access_token)
            existing.refresh_token = (
                encrypt_token(refresh_token) if refresh_token else None
            )
            existing.token_expires_at = expiry
            existing.is_connected = True
            existing.is_active = True

            self.db.commit()
            self.db.refresh(existing)

            return {
                "id": existing.id,
                "account_name": existing.account_name,
            }

        # ---------------------------------------
        # Create New Connected Account
        # ---------------------------------------

        account = SocialAccount(
            user_id=user_id,
            platform=platform,
            account_name=account_name,
            account_id=account_id,
            access_token=encrypt_token(access_token),
            refresh_token=(encrypt_token(refresh_token) if refresh_token else None),
            token_expires_at=expiry,
            is_connected=True,
            is_active=True,
        )

        self.db.add(account)

        self.db.commit()

        self.db.refresh(account)

        return {
            "id": account.id,
            "account_name": account.account_name,
        }

    # --------------------------------------------------
    # Refresh Token
    # --------------------------------------------------

    def refresh_token(
        self,
        platform: str,
        refresh_token: str,
    ):

        service = self.get_platform_service(platform)

        # Future implementation
        # LinkedIn currently does not support
        # standard OAuth refresh tokens.

        return {
            "access_token": "new_access_token",
            "expiry": None,
        }
