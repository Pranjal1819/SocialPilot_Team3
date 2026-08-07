# app/core/security.py

from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext


from .config import settings

# --------------------------------------
# Password Hashing
# --------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --------------------------------------
# Token Encryption
# --------------------------------------

cipher = Fernet(settings.ENCRYPTION_KEY.encode())


# --------------------------------------
# Password Functions
# --------------------------------------


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against hashed password
    """

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt
    """

    return pwd_context.hash(password)


# --------------------------------------
# JWT Functions
# --------------------------------------


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    """

    to_encode = data.copy()

    if expires_delta:

        expire = datetime.utcnow() + expires_delta

    else:

        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode JWT access token
    """

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None


# --------------------------------------
# Social Media Token Encryption
# --------------------------------------


def encrypt_token(token: str) -> str:
    """
    Encrypt OAuth access/refresh tokens
    before storing in database
    """

    if not token:
        return None

    encrypted = cipher.encrypt(token.encode())

    return encrypted.decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypt OAuth tokens before
    sending request to social APIs
    """

    if not encrypted_token:
        return None

    try:
        decrypted = cipher.decrypt(encrypted_token.encode())

        return decrypted.decode()

    except InvalidToken:
        raise Exception("Invalid encrypted token")
