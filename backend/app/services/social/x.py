import hashlib
import base64
import secrets
import requests
from pathlib import Path
from urllib.parse import urlencode

from app.core.config import settings


class XService:

    # ==================================================
    # PKCE Helpers
    # ==================================================

    def generate_pkce_pair(self):
        code_verifier = secrets.token_urlsafe(64)[:128]
        digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
        return code_verifier, code_challenge

    # ==================================================
    # OAuth
    # ==================================================

    def get_oauth_url(self, redirect_uri, state, code_challenge):

        params = {
            "response_type": "code",
            "client_id": settings.X_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "scope": "tweet.read tweet.write users.read offline.access media.write",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        return "https://twitter.com/i/oauth2/authorize?" + urlencode(params)

    # ==================================================
    # Exchange Authorization Code for Tokens
    # ==================================================

    def exchange_code(self, code, redirect_uri, code_verifier):

        response = requests.post(
            "https://api.twitter.com/2/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.X_CLIENT_ID,
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier,
            },
            auth=(settings.X_CLIENT_ID, settings.X_CLIENT_SECRET),
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"X token exchange failed: " f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # Refresh Access Token
    # ==================================================

    def refresh_access_token(self, refresh_token):

        if not refresh_token:
            raise Exception("X refresh token is missing")

        response = requests.post(
            "https://api.twitter.com/2/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.X_CLIENT_ID,
            },
            auth=(settings.X_CLIENT_ID, settings.X_CLIENT_SECRET),
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"X token refresh failed: " f"{response.status_code} - {response.text}"
            )

        data = response.json()

        access_token = data.get("access_token")

        if not access_token:
            raise Exception(
                "X token refresh succeeded but no access token was returned"
            )

        return data

    # ==================================================
    # Profile
    # ==================================================

    def get_profile(self, access_token):

        response = requests.get(
            "https://api.twitter.com/2/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"user.fields": "profile_image_url,username,name"},
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"X profile request failed: "
                f"{response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # TEXT POST
    # ==================================================

    def publish_post(self, access_token, text):

        response = requests.post(
            "https://api.twitter.com/2/tweets",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"text": text},
            timeout=20,
        )

        print("X Status:", response.status_code)
        print("X Response:", response.text)

        if response.status_code not in [200, 201]:
            raise Exception(f"X post failed: {response.status_code} - {response.text}")

        return response.json()

    # ==================================================
    # Media Upload — Images/GIFs (simple upload)
    # ==================================================

    def upload_image(self, access_token, file_path, media_type="image"):

        with open(file_path, "rb") as file:

            response = requests.post(
                "https://upload.twitter.com/1.1/media/upload.json",
                headers={"Authorization": f"Bearer {access_token}"},
                files={"media": file},
            )

        print("X Upload Status:", response.status_code)
        print("X Upload Headers:", response.headers)
        print("X Upload Body:", response.text)

        if not response.ok:
            raise Exception(
                f"X media upload failed: " f"{response.status_code} - {response.text}"
            )

        return response.json().get("media_id_string")

    # ==================================================
    # Media Upload — Video (chunked: INIT/APPEND/FINALIZE)
    # ==================================================

    def upload_video(self, access_token, file_path, media_type="video/mp4"):

        headers = {"Authorization": f"Bearer {access_token}"}

        total_bytes = Path(file_path).stat().st_size

        # ---------------- INIT ----------------

        init_response = requests.post(
            "https://upload.twitter.com/1.1/media/upload.json",
            headers=headers,
            data={
                "command": "INIT",
                "media_type": media_type,
                "total_bytes": total_bytes,
                "media_category": "tweet_video",
            },
        )

        if not init_response.ok:
            raise Exception(
                f"X video init failed: "
                f"{init_response.status_code} - {init_response.text}"
            )

        media_id = init_response.json()["media_id_string"]

        # ---------------- APPEND ----------------

        segment_id = 0
        chunk_size = 4 * 1024 * 1024  # 4MB chunks

        with open(file_path, "rb") as file:

            while True:

                chunk = file.read(chunk_size)

                if not chunk:
                    break

                append_response = requests.post(
                    "https://upload.twitter.com/1.1/media/upload.json",
                    headers=headers,
                    data={
                        "command": "APPEND",
                        "media_id": media_id,
                        "segment_index": segment_id,
                    },
                    files={"media": chunk},
                )

                if not append_response.ok:
                    raise Exception(
                        f"X video append failed: "
                        f"{append_response.status_code} - {append_response.text}"
                    )

                segment_id += 1

        # ---------------- FINALIZE ----------------

        finalize_response = requests.post(
            "https://upload.twitter.com/1.1/media/upload.json",
            headers=headers,
            data={
                "command": "FINALIZE",
                "media_id": media_id,
            },
        )

        if not finalize_response.ok:
            raise Exception(
                f"X video finalize failed: "
                f"{finalize_response.status_code} - {finalize_response.text}"
            )

        return media_id

    # ==================================================
    # TEXT + MEDIA POST
    # ==================================================

    def publish_media_post(self, access_token, text, media_id):

        response = requests.post(
            "https://api.twitter.com/2/tweets",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "media": {"media_ids": [media_id]},
            },
            timeout=20,
        )

        print("X Media Post Status:", response.status_code)
        print("X Media Post Response:", response.text)

        if response.status_code not in [200, 201]:
            raise Exception(
                f"X media post failed: {response.status_code} - {response.text}"
            )

        return response.json()

    # ==================================================
    # Media Upload — Multiple Images (2-4, X limit)
    # ==================================================

    def upload_images(self, access_token, file_paths):

        if not (2 <= len(file_paths) <= 4):
            raise Exception("X multi-image post requires 2 to 4 images")

        media_ids = []

        for file_path in file_paths:

            media_id = self.upload_image(access_token, file_path)

            media_ids.append(media_id)

        return media_ids

    # ==================================================
    # MULTI-IMAGE POST
    # ==================================================

    def publish_multi_image_post(self, access_token, text, media_ids):

        response = requests.post(
            "https://api.twitter.com/2/tweets",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "media": {"media_ids": media_ids},
            },
            timeout=20,
        )

        print("X Multi-Image Post Status:", response.status_code)
        print("X Multi-Image Post Response:", response.text)

        if response.status_code not in [200, 201]:
            raise Exception(
                f"X multi-image post failed: {response.status_code} - {response.text}"
            )

        return response.json()
