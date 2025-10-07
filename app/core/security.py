from datetime import UTC, datetime, timedelta
import hashlib
import os
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt

# Variables d'env
SECRET_KEY = os.getenv("SECRET_KEY", "ThisIsASecretKeyForDemoPurposesOnly")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def hash_password(password: str) -> str:
    salt = "opshub_salt_for_testing"
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    result = f"pbkdf2_sha256${salt}${hashed.hex()}"
    return result


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash.startswith("pbkdf2_sha256$"):
        return False

    try:
        _, salt, stored_hash = password_hash.split("$")
        hashed = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return hashed.hex() == stored_hash
    except (ValueError, TypeError):
        return False


def create_access_token(
    sub: str, extra: dict[str, Any] | None = None, expires_minutes: int | None = None
) -> str:
    to_encode: dict[str, Any] = {"sub": sub, "iat": datetime.now(tz=UTC)}
    if extra:
        to_encode.update(extra)
    expire = datetime.now(tz=UTC) + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def verify_token(token: str) -> dict[str, Any]:
    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


# Alias pour compatibilité avec le reste du code
def get_password_hash(password: str) -> str:
    return hash_password(password)
