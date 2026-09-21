from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class RoadResponse(BaseModel):
    id:int
    city_id:int
    osm_id:Optional[str] = None
    name:Optional[str] = None
    highway_type:Optional[str] = None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True)

class RoadGeoJSONResponse(BaseModel):
    id:int
    city_id:int
    osm_id:Optional[str] = None
    name:Optional[str] = None
    highway_type:Optional[str] = None
    is_active: bool
    geometry: dict[str, Any]

class NearestRoadResponse(BaseModel):
    id:int
    city_id:int
    osm_id: str | None
    name: str | None
    highway_type: str | None
    is_active: bool
    distance_meters: float | None
    geometry : dict