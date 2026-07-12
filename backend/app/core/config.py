from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    LINKEDIN_REDIRECT_URI: str

    class Config:
        env_file = ".env"


settings = Settings()