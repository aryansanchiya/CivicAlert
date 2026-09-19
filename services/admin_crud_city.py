# app/crud/city.py

from sqlalchemy.orm import Session

from models.city import City
from schemas.create_city import CityCreate, CityUpdate


def create_city(db: Session, city_data: CityCreate) -> City:
    city = City(
        name=city_data.name,
        state=city_data.state,
        country=city_data.country,
        osm_id=city_data.osm_id,
    )

    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def get_city(db: Session, city_id: int) -> City | None:
    return (
        db.query(City)
        .filter(City.id == city_id)
        .first()
    )


def get_cities(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[City]:

    return (
        db.query(City)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_city(
    db: Session,
    city_id: int,
    city_data: CityUpdate
) -> City | None:

    city = get_city(db, city_id)

    if city is None:
        return None

    update_data = city_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)

    return city


def delete_city(
    db: Session,
    city_id: int
) -> City | None:

    city = get_city(db, city_id)

    if city is None:
        return None

    db.delete(city)
    db.commit()

    return city