from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    LINKEDIN_REDIRECT_URI: str
    X_CLIENT_ID: str
    X_CLIENT_SECRET: str

    YOUTUBE_CLIENT_ID: str
    YOUTUBE_CLIENT_SECRET: str
    YOUTUBE_REDIRECT_URI: str

    ENCRYPTION_KEY: str
    SECRET_KEY: str
    DEBUG: bool

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Local disk media upload settings
    UPLOAD_DIR: str = "app/static/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    BASE_URL: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
