import time
import requests

from app.core.config import settings


class InstagramService:

    # ==================================================
    # OAuth — Authorization URL
    # ==================================================

    def get_oauth_url(self, redirect_uri):
        print("DEBUG INSTAGRAM CLIENT ID:", settings.INSTAGRAM_CLIENT_ID)

        scopes = (
            "instagram_business_basic,"
            "instagram_business_content_publish"
        )

        from urllib.parse import urlencode

        return "https://www.instagram.com/oauth/authorize?" + urlencode({
            "client_id": settings.INSTAGRAM_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scopes,
        })

    # ==================================================
    # Exchange Authorization Code for Tokens
    #
    # Instagram is a TWO-STEP exchange, unlike every other
    # platform here:
    #   1. Authorization code -> short-lived access token
    #      (valid ~1 hour)
    #   2. Short-lived token -> long-lived access token
    #      (valid ~60 days)
    #
    # This method does both steps internally so it still
    # returns a single dict, matching the shape
    # SocialIntegrationService.connect_account() expects
    # from every other service (access_token, expires_in).
    #
    # NOTE: Instagram has NO classic refresh_token. The
    # long-lived access token refreshes ITSELF (see
    # refresh_access_token below). To fit the existing
    # access_token/refresh_token pattern without rewriting
    # SocialIntegrationService, we return the long-lived
    # token as BOTH access_token and refresh_token here.
    # refresh_access_token() then treats the incoming
    # "refresh_token" argument as the long-lived token to
    # self-refresh — this is intentional, not a bug.
    # ==================================================

    def exchange_code(self, code, redirect_uri):

        # ---------- Step 1: code -> short-lived token ----------

        short_lived_response = requests.post(
            "https://api.instagram.com/oauth/access_token",
            data={
                "client_id": settings.INSTAGRAM_CLIENT_ID,
                "client_secret": settings.INSTAGRAM_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
                "code": code,
            },
            timeout=10,
        )

        print("Instagram Short-Lived Token Status:", short_lived_response.status_code)
        print("Instagram Short-Lived Token Response:", short_lived_response.text)

        if not short_lived_response.ok:
            raise Exception(
                f"Instagram short-lived token exchange failed: "
                f"{short_lived_response.status_code} - {short_lived_response.text}"
            )

        short_lived_data = short_lived_response.json()

        short_lived_token = short_lived_data.get("access_token")

        if not short_lived_token:
            raise Exception("Instagram did not return a short-lived access token")

        # ---------- Step 2: short-lived -> long-lived token ----------

        long_lived_response = requests.get(
            "https://graph.instagram.com/access_token",
            params={
                "grant_type": "ig_exchange_token",
                "client_secret": settings.INSTAGRAM_CLIENT_SECRET,
                "access_token": short_lived_token,
            },
            timeout=10,
        )

        print("Instagram Long-Lived Token Status:", long_lived_response.status_code)
        print("Instagram Long-Lived Token Response:", long_lived_response.text)

        if not long_lived_response.ok:
            raise Exception(
                f"Instagram long-lived token exchange failed: "
                f"{long_lived_response.status_code} - {long_lived_response.text}"
            )

        long_lived_data = long_lived_response.json()

        long_lived_token = long_lived_data.get("access_token")

        if not long_lived_token:
            raise Exception("Instagram did not return a long-lived access token")

        expires_in = long_lived_data.get("expires_in")  # ~5184000 seconds (60 days)

        return {
            "access_token": long_lived_token,
            "refresh_token": long_lived_token,
            "expires_in": expires_in,
        }

    # ==================================================
    # Refresh Access Token
    #
    # Instagram's long-lived tokens refresh themselves —
    # there is no separate refresh token to exchange.
    # The "refresh_token" passed in here IS the current
    # long-lived access token (see note above).
    # ==================================================

    def refresh_access_token(self, refresh_token):

        if not refresh_token:
            raise Exception("Instagram access token to refresh is missing")

        response = requests.get(
            "https://graph.instagram.com/refresh_access_token",
            params={
                "grant_type": "ig_refresh_token",
                "access_token": refresh_token,
            },
            timeout=10,
        )

        print("Instagram Token Refresh Status:", response.status_code)
        print("Instagram Token Refresh Response:", response.text)

        if not response.ok:
            raise Exception(
                f"Instagram token refresh failed: "
                f"{response.status_code} - {response.text}"
            )

        data = response.json()

        new_token = data.get("access_token")

        if not new_token:
            raise Exception(
                "Instagram token refresh succeeded but no access token was returned"
            )

        return {
            "access_token": new_token,
            "refresh_token": new_token,
            "expires_in": data.get("expires_in"),
        }

    # ==================================================
    # Profile
    # ==================================================

    def get_profile(self, access_token):

        response = requests.get(
            "https://graph.instagram.com/v21.0/me",
            params={
                "fields": "id,username,account_type",
                "access_token": access_token,
            },
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"Instagram profile request failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # PUBLISH MEDIA (two-step: create container, then publish)
    #
    # Requires media_url to be PUBLICLY reachable — Instagram's
    # servers fetch it directly, unlike LinkedIn/X/YouTube
    # which accept direct file uploads. A local
    # 127.0.0.1/localhost URL will fail here.
    #
    # media_type: "IMAGE" or "REELS" (video)
    # ==================================================

    def publish_media(
        self, access_token, ig_user_id, media_url, caption, media_type="IMAGE"
    ):

        # ---------------- Step 1: create container ----------------

        container_params = {
            "caption": caption,
            "access_token": access_token,
        }

        if media_type == "REELS":
            container_params["media_type"] = "REELS"
            container_params["video_url"] = media_url
        else:
            container_params["image_url"] = media_url

        container_response = requests.post(
            f"https://graph.instagram.com/v21.0/{ig_user_id}/media",
            params=container_params,
            timeout=20,
        )

        print("Instagram Container Create Status:", container_response.status_code)
        print("Instagram Container Create Response:", container_response.text)

        if not container_response.ok:
            raise Exception(
                f"Instagram media container creation failed: "
                f"{container_response.status_code} - {container_response.text}"
            )

        creation_id = container_response.json().get("id")

        if not creation_id:
            raise Exception("Instagram did not return a container creation id")

        # ---------------- Step 2: poll until ready (video only) ----------------

        if media_type == "REELS":

            for _ in range(30):  # up to ~5 minutes (30 x 10s)

                status_response = requests.get(
                    f"https://graph.instagram.com/v21.0/{creation_id}",
                    params={
                        "fields": "status_code",
                        "access_token": access_token,
                    },
                    timeout=10,
                )

                status_code = status_response.json().get("status_code")

                print(f"Instagram Container Status: {status_code}")

                if status_code == "FINISHED":
                    break

                if status_code == "ERROR":
                    raise Exception("Instagram failed to process the video container")

                time.sleep(10)

            else:

                raise Exception(
                    "Instagram video container did not finish processing in time"
                )

        # ---------------- Step 3: publish container ----------------

        publish_response = requests.post(
            f"https://graph.instagram.com/v21.0/{ig_user_id}/media_publish",
            params={
                "creation_id": creation_id,
                "access_token": access_token,
            },
            timeout=20,
        )

        print("Instagram Publish Status:", publish_response.status_code)
        print("Instagram Publish Response:", publish_response.text)

        if not publish_response.ok:
            raise Exception(
                f"Instagram media publish failed: "
                f"{publish_response.status_code} - {publish_response.text}"
            )

        return publish_response.json()
    
        # ==================================================
    # INSIGHTS (real analytics — requires
    # instagram_business_manage_insights scope, already
    # granted for this app's connected test accounts)
    # ==================================================

    def get_account_insights(self, access_token, ig_user_id):

        response = requests.get(
            f"https://graph.instagram.com/v21.0/{ig_user_id}/insights",
            params={
                "metric": "reach,profile_views,accounts_engaged",
                "period": "day",
                "access_token": access_token,
            },
            timeout=15,
        )

        print("Instagram Account Insights Status:", response.status_code)
        print("Instagram Account Insights Response:", response.text)

        if not response.ok:
            raise Exception(
                f"Instagram account insights request failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    def get_media_insights(self, access_token, media_id):

        response = requests.get(
            f"https://graph.instagram.com/v21.0/{media_id}/insights",
            params={
                "metric": "reach,likes,comments,saved,shares",
                "access_token": access_token,
            },
            timeout=15,
        )

        print("Instagram Media Insights Status:", response.status_code)
        print("Instagram Media Insights Response:", response.text)

        if not response.ok:
            raise Exception(
                f"Instagram media insights request failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()