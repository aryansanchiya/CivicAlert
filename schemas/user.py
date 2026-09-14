from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserCreate(BaseModel):
    tenant_id: UUID

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    role: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    tenant_id: UUID

    name: str

    email: EmailStr

    role: str

    status: UserStatus