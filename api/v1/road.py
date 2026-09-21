from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.road import Road
from schemas.road import RoadResponse, NearestRoadResponse, RoadGeoJSONResponse
import json
from geoalchemy2.functions import ST_AsGeoJSON, ST_Intersects, ST_MakeEnvelope
from schemas.road import RoadResponse, RoadGeoJSONResponse
from geoalchemy2 import Geography, functions as geo


router = APIRouter(
    prefix="/roads",    tags=["Roads"],
    responses={404: {"description": "Not found"}},
)

@router.get("/search", response_model=list[RoadResponse])
def search_roads(
    q:str = Query(..., min_length=2),
    city_id:int = Query(5),
    db:Session = Depends(get_db)
):
    statement = (
        select(Road).where(
            Road.city_id == city_id,
            Road.name.isnot(None),
            Road.name.ilike(f"%{q}%"),
            Road.is_active.is_(True),
        )
        .order_by(Road.name)
        .limit(20)
    )
    return db.scalars(statement).all()

@router.get(
    "/viewport",
    response_model=list[RoadGeoJSONResponse],
)
def get_roads_in_viewport(
    min_lon: float = Query(..., description="Minimum longitude"),
    min_lat: float = Query(..., description="Minimum latitude"),
    max_lon: float = Query(..., description="Maximum longitude"),
    max_lat: float = Query(..., description="Maximum latitude"),
    city_id: int = Query(..., description="City ID"),
    db: Session = Depends(get_db),
):
    viewport = ST_MakeEnvelope(
        min_lon,
        min_lat,
        max_lon,
        max_lat,
        4326,
    )

    statement = (
        select(
            Road.id,
            Road.city_id,
            Road.osm_id,
            Road.name,
            Road.highway_type,
            Road.is_active,
            ST_AsGeoJSON(Road.geometry).label("geometry"),
        )
        .where(
            Road.city_id == city_id,
            Road.is_active.is_(True),
            Road.geometry.is_not(None),
            ST_Intersects(Road.geometry, viewport),
        )
    )

    results = db.execute(statement).all()

    roads = []

    for row in results:
        roads.append(
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

    return roads

@router.get(
    "/nearest",
    response_model=NearestRoadResponse,
)
def get_nearest_road(
    longitude: float = Query(..., description="Longitude"),
    latitude: float = Query(..., description="Latitude"),
    city_id: int = Query(..., description="City ID"),
    db: Session = Depends(get_db),
):
    point = geo.ST_SetSRID(
        geo.ST_MakePoint(longitude, latitude),
        4326,
    )

    distance = geo.ST_Distance(
        Road.geometry.cast(Geography),
        point.cast(Geography),
    ).label("distance_meters")

    statement = (
        select(
            Road.id,
            Road.city_id,
            Road.osm_id,
            Road.name,
            Road.highway_type,
            Road.is_active,
            distance,
            geo.ST_AsGeoJSON(Road.geometry).label("geometry"),
        )
        .where(
            Road.city_id == city_id,
            Road.is_active.is_(True),
            Road.geometry.is_not(None),
        )
        .order_by(distance)
        .limit(1)
    )

    row = db.execute(statement).first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="No road found for this city.",
        )

    return {
        "id": row.id,
        "city_id": row.city_id,
        "osm_id": row.osm_id,
        "name": row.name,
        "highway_type": row.highway_type,
        "is_active": row.is_active,
        "distance_meters": row.distance_meters,
        "geometry": json.loads(row.geometry),
    }