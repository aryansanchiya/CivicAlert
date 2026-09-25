from typing import Any
from pydantic import BaseModel, Field

class IncidentPreviewRequest(BaseModel):
    city_id: int = Field(..., description="The ID of the city for which to retrieve incident previews.")

    geometry: dict[str, Any] = Field(..., description="The geometry of the area to filter incidents. This should be a GeoJSON object.")


class IncidentPreviewRoad(BaseModel):
    id: int
    city_id :int
    osm_id: str | None
    name : str | None
    highway_type : str | None
    is_active : bool
    geometry : dict[str, Any]

class IncidentPreviewResponse(BaseModel):
    affected_road_count : int
    affected_roads : list[IncidentPreviewRoad]
    