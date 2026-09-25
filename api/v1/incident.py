import json

from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import from_shape
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from shapely.geometry import shape

from database.dependencies import get_db
from models.road import Road
from schemas.incident import (
    IncidentPreviewRequest,
    IncidentPreviewResponse,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "/preview",
    response_model=IncidentPreviewResponse,
)
def preview_incident(
    payload: IncidentPreviewRequest,
    db: Session = Depends(get_db),
):
    # Convert incoming GeoJSON to Shapely geometry
    try:
        incident_shape = shape(payload.geometry)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid GeoJSON geometry: {exc}",
        )

    # Only Polygon and MultiPolygon are allowed
    if incident_shape.geom_type not in {"Polygon", "MultiPolygon"}:
        raise HTTPException(
            status_code=400,
            detail="Incident geometry must be a Polygon or MultiPolygon.",
        )

    if incident_shape.is_empty:
        raise HTTPException(
            status_code=400,
            detail="Incident geometry cannot be empty.",
        )

    if not incident_shape.is_valid:
        raise HTTPException(
            status_code=400,
            detail="Incident geometry is invalid.",
        )

    # Convert Shapely geometry to PostGIS geometry
    incident_geometry = from_shape(
        incident_shape,
        srid=4326,
    )

    # Find roads intersecting the selected incident area
    statement = (
        select(
            Road.id,
            Road.city_id,
            Road.osm_id,
            Road.name,
            Road.highway_type,
            Road.is_active,
            func.ST_AsGeoJSON(Road.geometry).label("geometry"),
        )
        .where(
            Road.city_id == payload.city_id,
            Road.is_active.is_(True),
            Road.geometry.is_not(None),
            func.ST_Intersects(
                Road.geometry,
                incident_geometry,
            ),
        )
    )

    results = db.execute(statement).all()

    affected_roads = []

    for row in results:
        affected_roads.append(
            {
                "id": row.id,
                "city_id": row.city_id,
                "osm_id": row.osm_id,
                "name": row.name,
                "highway_type": row.highway_type,
                "is_active": row.is_active,
                "geometry": json.loads(row.geometry),
            }
        )

    return {
        "affected_road_count": len(affected_roads),
        "affected_roads": affected_roads,
    }