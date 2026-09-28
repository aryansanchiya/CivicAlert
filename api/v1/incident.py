import json

from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import from_shape
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from shapely.geometry import shape

from database.dependencies import get_db
from models.road import Road
from models.incident_road import IncidentRoad
from models.incident import Incident
from schemas.incident import (
    IncidentPreviewRequest,
    IncidentPreviewResponse,
    IncidentCreateRequest,
    IncidentCreateResponse
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

@router.post(
    "",
    response_model=IncidentCreateResponse,
)
def create_incident(
    payload:IncidentCreateRequest,
    db:Session = Depends(get_db),
):
    try:
        incident_shape = shape(payload.geometry)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            details=f"Invalic GeoJson geometry : {exc}"
        )
    
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

    incident_geometry = from_shape(
        incident_shape,
        srid=4326,
    )

    try:
        # ---------------------------------------------------------
        # 1. Find affected roads
        # ---------------------------------------------------------

        statement = (
            select(Road.id)
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

        affected_road_ids = db.scalars(statement).all()

        # ---------------------------------------------------------
        # 2. Create incident
        # ---------------------------------------------------------

        incident = Incident(
            city_id=payload.city_id,
            title=payload.title,
            description=payload.description,
            incident_type=payload.incident_type,
            severity=payload.severity,
            geometry=incident_geometry,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            is_active=True,
        )

        db.add(incident)

        # Flush so incident.id becomes available
        db.flush()

        # ---------------------------------------------------------
        # 3. Store affected roads
        # ---------------------------------------------------------

        incident_roads = [
            IncidentRoad(
                incident_id=incident.id,
                road_id=road_id,
            )
            for road_id in affected_road_ids
        ]

        db.add_all(incident_roads)

        # ---------------------------------------------------------
        # 4. Commit everything together
        # ---------------------------------------------------------

        db.commit()

        db.refresh(incident)

        return {
            "id": incident.id,
            "city_id": incident.city_id,
            "title": incident.title,
            "description": incident.description,
            "incident_type": incident.incident_type,
            "severity": incident.severity,
            "starts_at": incident.starts_at,
            "ends_at": incident.ends_at,
            "is_active": incident.is_active,
            "affected_road_count": len(affected_road_ids),
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to register incident.",
        )
