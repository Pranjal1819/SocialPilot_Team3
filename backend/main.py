from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import requests

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User


app = FastAPI()


@app.get("/root")
def root():
    return {"message": "Hello"}


# Step 1: Redirect to LinkedIn login
@app.get("/login/linkedin")
def linkedin_login():

    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": "openid profile email"
    }

    linkedin_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        + urlencode(params)
    )

    return RedirectResponse(url=linkedin_url)



# Step 2: LinkedIn callback
@app.get("/auth/linkedin/callback")
def linkedin_callback(code: str = None, error: str = None):

    if error:
        return {
            "error": error
        }


    # Get access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"


    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET
    }


    token_response = requests.post(
        token_url,
        data=token_data
    )


    token_json = token_response.json()

    access_token = token_json.get("access_token")


    if not access_token:
        return {
            "error": "Access token generation failed",
            "response": token_json
        }



    # Get LinkedIn user information

    user_response = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )


    user_data = user_response.json()


    # PostgreSQL connection

    db: Session = SessionLocal()


    linkedin_id = user_data.get("sub")
    email = user_data.get("email")
    name = user_data.get("name")
    picture = user_data.get("picture")


    # Check existing user

    existing_user = db.query(User).filter(
        User.linkedin_id == linkedin_id
    ).first()



    if existing_user:

        user = existing_user


    else:

        new_user = User(
            linkedin_id=linkedin_id,
            name=name,
            email=email,
            profile_picture=picture,
            password=None
        )


        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user = new_user



    db.close()



    return {
        "message": "LinkedIn login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "profile_picture": user.profile_picture
    }