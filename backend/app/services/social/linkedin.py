import requests
from urllib.parse import urlencode

from app.core.config import settings


class LinkedInService:

    # --------------------------------------
    # Generate LinkedIn OAuth URL
    # --------------------------------------

    def get_oauth_url(self, redirect_uri):

        params = {
            "response_type": "code",
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "scope": "openid profile email w_member_social",
        }

        return "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)

    # --------------------------------------
    # Exchange OAuth Code For Access Token
    # --------------------------------------

    def exchange_code(self, code, redirect_uri):

        url = "https://www.linkedin.com/oauth/v2/accessToken"

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
        }

        response = requests.post(url, data=data, timeout=10)

        if not response.ok:

            raise Exception(f"LinkedIn token exchange failed: {response.text}")

        return response.json()

    # --------------------------------------
    # Get LinkedIn User Profile
    # --------------------------------------

    def get_profile(self, access_token):

        url = "https://api.linkedin.com/v2/userinfo"

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers, timeout=10)

        if not response.ok:

            raise Exception(f"LinkedIn profile fetch failed: {response.text}")

        return response.json()

    # --------------------------------------
    # Publish LinkedIn Text Post
    # --------------------------------------

    def publish_post(self, access_token, author_id, text):

        url = "https://api.linkedin.com/v2/ugcPosts"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

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

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        print("LinkedIn Status:", response.status_code)

        print("LinkedIn Response:", response.text)

        if response.status_code not in [200, 201]:

            raise Exception(f"LinkedIn publish failed: {response.text}")

        # LinkedIn returns:
        #
        # {
        #    "id":"urn:li:share:7488501498956591105"
        # }
        #
        # Return JSON directly

        return response.json()
