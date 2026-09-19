# app/routers/city.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas import city
from schemas.create_city import (
    CityCreate,
    CityResponse,
    CityUpdate,
)
from services.admin_crud_city import (
    create_city,
    delete_city,
    get_cities,
    get_city,
    update_city,
)


router = APIRouter(
    prefix="/api/v1/cities",
    tags=["Admin Crud Cities"]
)


@router.post(
    "/",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_city_endpoint(
    city_data: CityCreate,
    db: Session = Depends(get_db),
):
    return create_city(db, city_data)


@router.get(
    "/",
    response_model=list[CityResponse]
)
def list_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_cities(
        db,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{city_id}",
    response_model=CityResponse
)
def get_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = get_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return city


@router.put(
    "/{city_id}",
    response_model=CityResponse
)
def update_city_endpoint(
    city_id: int,
    city_data: CityUpdate,
    db: Session = Depends(get_db),
):
    city = update_city(
        db,
        city_id,
        city_data
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = delete_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return None