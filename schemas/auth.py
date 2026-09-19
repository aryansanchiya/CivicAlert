from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

class AuthUserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    email: EmailStr
    role: str
    status: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: AuthUserResponse