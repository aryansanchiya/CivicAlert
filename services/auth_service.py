from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.tenant import Tenant
from models.user import User
from schemas.auth import LoginRequest
from utils.security import create_access_token, verify_password


def authenticate_user(
    db: Session,
    login_data: LoginRequest,
) -> tuple[User, str]:

    email = login_data.email.strip().lower()

    # 1. Find user by email
    user = db.scalar(
        select(User).where(
            func.lower(User.email) == email
        )
    )

    if not user:
        raise ValueError("Invalid email or password.")

    # 2. Verify password
    if not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise ValueError("Invalid email or password.")

    # 3. Check user status
    if user.status != "active":
        raise ValueError("User account is not active.")

    # 4. Find user's tenant
    tenant = db.scalar(
        select(Tenant).where(
            Tenant.id == user.tenant_id
        )
    )

    if not tenant:
        raise ValueError(
            "Government organization not found."
        )

    # 5. Check tenant status
    if tenant.status != "active":
        raise ValueError(
            "Government organization is not active."
        )

    # 6. Generate JWT access token
    access_token = create_access_token(
        user_id=str(user.id),
        tenant_id=str(user.tenant_id),
        role=user.role,
    )

    return user, access_token