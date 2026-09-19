# app/schemas/city.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    name: str
    state: str
    country: str = "India"
    osm_id: str | None = None


class CityUpdate(BaseModel):
    name: str | None = None
    state: str | None = None
    country: str | None = None
    osm_id: str | None = None
    is_active: bool | None = None


class CityResponse(BaseModel):
    id: int
    name: str
    state: str
    country: str
    osm_id: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)