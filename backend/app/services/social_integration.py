from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.social_account import SocialAccount
from app.services.social.linkedin import LinkedInService
from app.services.social.x import XService
from app.services.social.youtube import YouTubeService
from app.core.security import encrypt_token, decrypt_token
from app.services.social.instagram import InstagramService


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

        if platform == "x":
            return XService()

        if platform == "youtube":
            return YouTubeService()

        if platform == "instagram":
            return InstagramService()

        raise Exception(f"Unsupported platform: {platform}")

    # --------------------------------------------------
    # Generate OAuth URL
    # --------------------------------------------------

    def get_oauth_url(
        self,
        platform: str,
        redirect_uri: str,
        state: str = None,
        code_challenge: str = None,
    ):

        service = self.get_platform_service(platform)

        if platform.lower() == "x":
            return service.get_oauth_url(redirect_uri, state, code_challenge)

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
        code_verifier: str = None,
    ):

        platform = platform.lower()

        service = self.get_platform_service(platform)

        # ---------------------------------------
        # Exchange OAuth Code
        # ---------------------------------------

        if platform == "x":
            token_data = service.exchange_code(auth_code, redirect_uri, code_verifier)
        else:
            token_data = service.exchange_code(auth_code, redirect_uri)

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")

        if not access_token:
            raise Exception("Failed to obtain access token")

        # ---------------------------------------
        # Fetch User Profile
        # ---------------------------------------

        profile = service.get_profile(access_token)

        if platform == "x":
            user_data = profile.get("data", {})
            account_name = (
                user_data.get("name") or user_data.get("username") or "X User"
            )
            account_id = user_data.get("id")
        elif platform == "instagram":
            account_name = profile.get("username") or "Instagram User"
            account_id = profile.get("id")
        else:
            account_name = (
                profile.get("name")
                or profile.get("localizedFirstName")
                or f"{platform.title()} User"
            )
            account_id = profile.get("sub") or profile.get("id")

        if not account_id:
            raise Exception(f"Unable to determine {platform} account ID")

        # ---------------------------------------
        # Prevent Duplicate Connection
        # ---------------------------------------

        existing = (
            self.db.query(SocialAccount)
            .filter(
                SocialAccount.platform == platform,
                SocialAccount.account_id == account_id,
            )
            .first()
        )

        # ---------------------------------------
        # Calculate Token Expiry
        # ---------------------------------------

        expiry = None

        if expires_in:
            expiry = datetime.utcnow() + timedelta(seconds=int(expires_in))

        # ---------------------------------------
        # Existing Account
        # ---------------------------------------

        if existing:

            if existing.user_id != user_id:

                raise Exception(
                    f"This {platform} account is already connected to another user."
                )

            existing.account_name = account_name

            existing.access_token = encrypt_token(access_token)

            if refresh_token:
                existing.refresh_token = encrypt_token(refresh_token)

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

        if not refresh_token:
            raise Exception("Refresh token is missing")

        decrypted_refresh_token = decrypt_token(refresh_token)

        if not decrypted_refresh_token:
            raise Exception("Unable to decrypt refresh token")

        token_data = service.refresh_access_token(decrypted_refresh_token)

        new_access_token = token_data.get("access_token")

        new_refresh_token = token_data.get("refresh_token")

        expires_in = token_data.get("expires_in")

        if not new_access_token:
            raise Exception(f"{platform} did not return a new access token")

        expiry = None

        if expires_in:

            expiry = datetime.utcnow() + timedelta(seconds=int(expires_in))

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "expiry": expiry,
        }
