from sqlalchemy.orm import Session
import requests
from app.models.social_account import SocialAccount

class SocialIntegrationService:
    def __init__(self, db: Session):
        self.db = db
    
    def connect_account(self, platform: str, auth_code: str, user_id: int):
        # Simplified OAuth flow - in production, implement full OAuth 2.0
        if platform == "facebook":
            token_data = self._get_facebook_token(auth_code)
            account_id = token_data.get("user_id")
            account_name = "Facebook User"  # Fetch from Graph API
            
        elif platform == "instagram":
            token_data = self._get_instagram_token(auth_code)
            account_id = token_data.get("user_id")
            account_name = "Instagram User"
            
        elif platform == "linkedin":
            token_data = self._get_linkedin_token(auth_code)
            account_id = token_data.get("user_id")
            account_name = "LinkedIn User"
            
        elif platform == "twitter":
            token_data = self._get_twitter_token(auth_code)
            account_id = token_data.get("user_id")
            account_name = "Twitter User"
        else:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Save to database
        social_account = SocialAccount(
            user_id=user_id,
            platform=platform,
            account_id=account_id,
            account_name=account_name,
            access_token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            token_expiry=token_data.get("expiry")
        )
        self.db.add(social_account)
        self.db.commit()
        self.db.refresh(social_account)
        
        return {
            "id": social_account.id,
            "platform": platform,
            "account_name": account_name
        }
    
    def _get_facebook_token(self, auth_code):
        # Implement Facebook OAuth token exchange
        return {"access_token": "facebook_token_123", "user_id": "fb_user_123"}
    
    def _get_instagram_token(self, auth_code):
        return {"access_token": "instagram_token_123", "user_id": "ig_user_123"}
    
    def _get_linkedin_token(self, auth_code):
        return {"access_token": "linkedin_token_123", "user_id": "li_user_123"}
    
    def _get_twitter_token(self, auth_code):
        return {"access_token": "twitter_token_123", "user_id": "tw_user_123"}