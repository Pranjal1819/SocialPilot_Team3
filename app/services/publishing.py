from sqlalchemy.orm import Session
import requests
from datetime import datetime
from app.models.post import Post
from app.models.social_account import SocialAccount

class PublishingService:
    def __init__(self, db: Session):
        self.db = db
    
    def publish_post(self, post_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return {"error": "Post not found"}
        
        # Get social account
        social_account = self.db.query(SocialAccount).filter(
            SocialAccount.user_id == post.user_id,
            SocialAccount.platform == post.platform,
            SocialAccount.is_active == True
        ).first()
        
        if not social_account:
            post.status = "failed"
            self.db.commit()
            return {"error": "No active social account found"}
        
        try:
            # Platform-specific publishing logic
            if post.platform == "facebook":
                result = self._publish_to_facebook(post, social_account)
            elif post.platform == "instagram":
                result = self._publish_to_instagram(post, social_account)
            elif post.platform == "linkedin":
                result = self._publish_to_linkedin(post, social_account)
            elif post.platform == "twitter":
                result = self._publish_to_twitter(post, social_account)
            else:
                result = {"error": "Unsupported platform"}
            
            if result.get("id"):
                post.status = "published"
                post.published_time = datetime.now()
                post.external_post_id = result["id"]
                self.db.commit()
                return {"success": True, "external_id": result["id"]}
            else:
                post.status = "failed"
                self.db.commit()
                return {"error": result.get("error", "Publishing failed")}
                
        except Exception as e:
            post.status = "failed"
            self.db.commit()
            return {"error": str(e)}
    
    def _publish_to_facebook(self, post, account):
        # Facebook Graph API implementation
        url = f"https://graph.facebook.com/v18.0/{account.account_id}/feed"
        payload = {
            "message": post.content,
            "access_token": account.access_token
        }
        response = requests.post(url, data=payload)
        return response.json()
    
    def _publish_to_instagram(self, post, account):
        # Instagram Graph API implementation
        # Simplified - in production, handle media uploads separately
        url = f"https://graph.facebook.com/v18.0/{account.account_id}/media"
        payload = {
            "image_url": post.media_urls[0] if post.media_urls else None,
            "caption": post.content,
            "access_token": account.access_token
        }
        response = requests.post(url, data=payload)
        return response.json()
    
    def _publish_to_linkedin(self, post, account):
        # LinkedIn API implementation
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {"Authorization": f"Bearer {account.access_token}"}
        payload = {
            "author": f"urn:li:person:{account.account_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": post.content},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    
    def _publish_to_twitter(self, post, account):
        # Twitter API v2 implementation
        url = "https://api.twitter.com/2/tweets"
        headers = {"Authorization": f"Bearer {account.access_token}"}
        payload = {"text": post.content}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()