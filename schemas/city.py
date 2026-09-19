# app/schemas/city.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    state: str
    country: str = "India"


class CityCreate(CityBase):
    osm_id: str | None = None


class CityResponse(CityBase):
    id: int
    osm_id: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)