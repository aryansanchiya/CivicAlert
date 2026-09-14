from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.user import UserCreate, UserResponse
from services.user_service import register_user


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_government_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:

        user = register_user(
            db=db,
            user_data=user_data,
        )

        return user

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )