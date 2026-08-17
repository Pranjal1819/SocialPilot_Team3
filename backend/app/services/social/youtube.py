import requests
from pathlib import Path
from urllib.parse import urlencode

from app.core.config import settings


class YouTubeService:

    # ==================================================
    # OAuth
    # ==================================================

    def get_oauth_url(self, redirect_uri):

        params = {
            "client_id": settings.YOUTUBE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": (
                "https://www.googleapis.com/auth/youtube.upload "
                "https://www.googleapis.com/auth/youtube.readonly "
                "openid email profile"
            ),
            "access_type": "offline",
            "prompt": "consent",
        }

        return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

    # ==================================================
    # Exchange Authorization Code for Tokens
    # ==================================================

    def exchange_code(self, code, redirect_uri):

        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YOUTUBE_CLIENT_ID,
                "client_secret": settings.YOUTUBE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
            },
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"YouTube token exchange failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # Refresh Access Token
    # ==================================================

    def refresh_access_token(self, refresh_token):

        if not refresh_token:
            raise Exception("YouTube refresh token is missing")

        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.YOUTUBE_CLIENT_ID,
                "client_secret": settings.YOUTUBE_CLIENT_SECRET,
            },
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"YouTube token refresh failed: "
                f"{response.status_code} - {response.text}"
            )

        data = response.json()

        # Note: Google does not always return a new refresh_token on
        # refresh — SocialIntegrationService.connect_account() already
        # handles this correctly (only overwrites refresh_token if a
        # new one is present), so no special handling needed here.

        access_token = data.get("access_token")

        if not access_token:
            raise Exception(
                "YouTube token refresh succeeded but no access token " "was returned"
            )

        return data

    # ==================================================
    # Profile
    # ==================================================

    def get_profile(self, access_token):

        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"YouTube profile request failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # VIDEO UPLOAD (resumable upload: INIT then PUT bytes)
    #
    # YouTube only supports video content — there is no
    # text-only, image, or document post type on this
    # platform, unlike LinkedIn/X. So there is only one
    # publish method here, not a family of them per media
    # type the way LinkedInService has.
    # ==================================================

    def publish_video(self, access_token, file_path, title, description=""):

        total_bytes = Path(file_path).stat().st_size

        # ---------------- INIT resumable session ----------------

        init_response = requests.post(
            "https://www.googleapis.com/upload/youtube/v3/videos"
            "?uploadType=resumable&part=snippet,status",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json; charset=UTF-8",
                "X-Upload-Content-Type": "video/*",
                "X-Upload-Content-Length": str(total_bytes),
            },
            json={
                "snippet": {
                    "title": title,
                    "description": description,
                },
                "status": {
                    "privacyStatus": "public",
                },
            },
            timeout=20,
        )

        print("YouTube Upload Init Status:", init_response.status_code)
        print("YouTube Upload Init Response:", init_response.text)

        if not init_response.ok:
            raise Exception(
                f"YouTube upload init failed: "
                f"{init_response.status_code} - {init_response.text}"
            )

        upload_url = init_response.headers.get("Location")

        if not upload_url:
            raise Exception("YouTube upload init did not return a resumable upload URL")

        # ---------------- Upload the file bytes ----------------

        with open(file_path, "rb") as file:

            upload_response = requests.put(
                upload_url,
                headers={
                    "Content-Type": "video/*",
                    "Content-Length": str(total_bytes),
                },
                data=file,
                timeout=None,
            )

        print("YouTube Upload Status:", upload_response.status_code)
        print("YouTube Upload Response:", upload_response.text)

        if not upload_response.ok:
            raise Exception(
                f"YouTube video upload failed: "
                f"{upload_response.status_code} - {upload_response.text}"
            )

        return upload_response.json()
