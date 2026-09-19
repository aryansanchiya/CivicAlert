from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.auth import LoginRequest, LoginResponse, AuthUserResponse
from services.auth_service import authenticate_user
from api.v1.dependencies.auth import get_current_user
from models.user import User



router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        user, access_token = authenticate_user(
            db=db,
            login_data=login_data,
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600,
            user={
                "id": user.id,
                "tenant_id": user.tenant_id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            },
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

@router.get(
    "/me",
    response_model=AuthUserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user