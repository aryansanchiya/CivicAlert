from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime

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


class IncidentCreateRequest(BaseModel):
    city_id: int = Field(
        ...,
        description="City ID associated with the incident.",
    )

    title: str = Field(
        ...,
        max_length=200,
    )

    description: str | None = None

    incident_type: str = Field(
        ...,
        description="Type of incident, for example FLOOD, ROAD_CLOSURE, ACCIDENT.",
    )

    severity: str = Field(
        ...,
        description="Incident severity, for example LOW, MEDIUM, HIGH, CRITICAL.",
    )

    geometry: dict[str, Any] = Field(
        ...,
        description="GeoJSON Polygon or MultiPolygon representing the affected area.",
    )

    starts_at: datetime

    ends_at: datetime | None = None


class IncidentCreateResponse(BaseModel):
    id: int
    city_id: int
    title: str
    description: str | None
    incident_type: str
    severity: str
    starts_at: datetime
    ends_at: datetime | None
    is_active: bool
    affected_road_count: int
    