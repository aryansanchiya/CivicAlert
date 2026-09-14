from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.tenant import Tenant
from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    # --------------------------------------------------
    # 1. Normalize input
    # --------------------------------------------------

    name = " ".join(
        user_data.name.strip().split()
    )

    email = user_data.email.strip().lower()

    role = " ".join(
        user_data.role.strip().split()
    )


    # --------------------------------------------------
    # 2. Check that tenant exists
    # --------------------------------------------------

    tenant = db.scalar(
        select(Tenant).where(
            Tenant.id == user_data.tenant_id
        )
    )

    if not tenant:
        raise ValueError(
            "Government organization not found."
        )


    # --------------------------------------------------
    # 3. Check tenant status
    # --------------------------------------------------

    if tenant.status != "active":
        raise ValueError(
            "Government organization is not active."
        )


    # --------------------------------------------------
    # 4. Check duplicate email
    # --------------------------------------------------

    existing_user = db.scalar(
        select(User).where(
            func.lower(User.email) == email
        )
    )

    if existing_user:
        raise ValueError(
            "A user with this email already exists."
        )


    # --------------------------------------------------
    # 5. Hash password
    # --------------------------------------------------

    password_hash = hash_password(
        user_data.password
    )


    # --------------------------------------------------
    # 6. Create user
    # --------------------------------------------------

    user = User(
        tenant_id=user_data.tenant_id,
        name=name,
        email=email,
        password_hash=password_hash,
        role=role,
        status="active",
    )


    # --------------------------------------------------
    # 7. Save user
    # --------------------------------------------------

    db.add(user)

    db.commit()

    db.refresh(user)

    return user