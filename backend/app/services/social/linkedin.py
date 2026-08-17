import requests
from urllib.parse import urlencode

from app.core.config import settings


class LinkedInService:

    # ==================================================
    # OAuth
    # ==================================================

    def get_oauth_url(self, redirect_uri):

        params = {
            "response_type": "code",
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "scope": "openid profile email w_member_social",
        }

        return "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)

    # ==================================================
    # Exchange Authorization Code for Tokens
    # ==================================================

    def exchange_code(self, code, redirect_uri):

        response = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
            },
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"LinkedIn token exchange failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # Refresh Access Token
    # ==================================================

    def refresh_access_token(self, refresh_token):

        if not refresh_token:
            raise Exception("LinkedIn refresh token is missing")

        response = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            },
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"LinkedIn token refresh failed: "
                f"{response.status_code} - {response.text}"
            )

        data = response.json()

        access_token = data.get("access_token")

        if not access_token:
            raise Exception(
                "LinkedIn token refresh succeeded but no access token " "was returned"
            )

        return data

    # ==================================================
    # Profile
    # ==================================================

    def get_profile(self, access_token):

        response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"LinkedIn profile request failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # TEXT POST
    # ==================================================

    def publish_post(self, access_token, author_id, text):

        payload = {
            "author": f"urn:li:person:{author_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        return self._send_post(access_token, payload)

    # ==================================================
    # REGISTER MEDIA
    # ==================================================

    def register_media(self, access_token, author_id, media_type):

        recipes = {
            "image": "urn:li:digitalmediaRecipe:feedshare-image",
            "gif": "urn:li:digitalmediaRecipe:feedshare-image",
            "video": "urn:li:digitalmediaRecipe:feedshare-video",
            "document": "urn:li:digitalmediaRecipe:feedshare-document",
        }

        if media_type == "audio":
            raise Exception("LinkedIn does not support audio posts")

        if media_type not in recipes:
            raise Exception(f"Unsupported media type {media_type}")

        payload = {
            "registerUploadRequest": {
                "recipes": [recipes[media_type]],
                "owner": f"urn:li:person:{author_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }

        response = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )

        if not response.ok:
            raise Exception(
                f"LinkedIn media registration failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # Upload File
    # ==================================================

    def upload_media_file(self, access_token, upload_url, file_path):

        with open(file_path, "rb") as file:

            response = requests.put(
                upload_url,
                headers={"Authorization": f"Bearer {access_token}"},
                data=file,
                timeout=120,
            )

        if response.status_code not in [200, 201]:

            raise Exception(
                f"LinkedIn media upload failed: "
                f"{response.status_code} - {response.text}"
            )

        return True

    # ==================================================
    # Single Media
    # ==================================================

    def publish_media_post(self, access_token, author_id, text, asset_urn, media_type):

        category_map = {
            "image": "IMAGE",
            "gif": "IMAGE",
            "video": "VIDEO",
            "document": "DOCUMENT",
        }

        if media_type == "audio":

            raise Exception("Audio publishing is not supported by LinkedIn")

        category = category_map.get(media_type)

        if not category:

            raise Exception(f"Unsupported media {media_type}")

        payload = {
            "author": f"urn:li:person:{author_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": category,
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn,
                            "title": {"text": "Uploaded Media"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        return self._send_post(access_token, payload)

    # ==================================================
    # Carousel (PDF based)
    # ==================================================

    def publish_carousel_post(self, access_token, author_id, text, asset_urn):

        payload = {
            "author": f"urn:li:person:{author_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "DOCUMENT",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn,
                            "title": {"text": "Carousel Document"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        return self._send_post(access_token, payload)

    # ==================================================
    # Common API
    # ==================================================

    def _send_post(self, access_token, payload):

        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            json=payload,
            timeout=20,
        )

        print("LinkedIn Status:", response.status_code)

        print("LinkedIn Response:", response.text)

        if response.status_code not in [200, 201]:

            raise Exception(
                f"LinkedIn post failed: " f"{response.status_code} - {response.text}"
            )

        return response.json()
