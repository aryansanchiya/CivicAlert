from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
import os


password_hash = PasswordHash.recommended()


# -------------------------
# Password Hashing
# -------------------------

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# -------------------------
# JWT Configuration
# -------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "x3yOh-2pk8HC60zIrIiA1WUI7anu9Mgkvib9LuM_AHA")  # Default value for development/testing    

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# -------------------------
# JWT Creation
# -------------------------

def create_access_token(
    user_id: str,
    tenant_id: str,
    role: str,
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# -------------------------
# JWT Verification
# -------------------------

def decode_access_token(token: str) -> dict:

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )