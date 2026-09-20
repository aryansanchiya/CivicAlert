import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from database.session import SessionLocal
from models.city import City
from models.road import Road
from geoalchemy2.shape import from_shape
from shapely.geometry import LineString

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

BHAVNAGAR_DISTRICT_RELATION_ID = 8259844

ROAD_TYPES = [
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "unclassified",
    "living_street",
]


def fetch_bhavnagar_roads():
    highway_regex = "|".join(ROAD_TYPES)

    query = f"""
    [out:json][timeout:180];

    rel({BHAVNAGAR_DISTRICT_RELATION_ID});

    map_to_area -> .bhavnagar;

    way
      ["highway"~"^({highway_regex})$"]
      (area.bhavnagar);

    out tags geom;
    """

    response = requests.post(
    OVERPASS_URL,
    data={"data": query},
    headers={
        "User-Agent": "CivicAlertSystem/1.0",
    },
    timeout=200,

)

    response.raise_for_status()

    return response.json()


def test_insert_one_road(data):
    db = SessionLocal()

    try:
        # Find Bhavnagar city
        city = (
            db.query(City)
            .filter(City.name == "Bhavnagar")
            .first()
        )

        if not city:
            raise Exception("Bhavnagar city not found in database")

        print(f"Bhavnagar city ID: {city.id}")

        # Take first road from Overpass response
        road_data = data["elements"][0]

        osm_id = str(road_data["id"])
        tags = road_data.get("tags", {})
        geometry = road_data.get("geometry", [])

        # Convert OSM coordinates:
        # OSM -> lat/lon
        # PostGIS -> lon/lat
        coordinates = [
            (point["lon"], point["lat"])
            for point in geometry
        ]

        line = LineString(coordinates)

        road = Road(
            city_id=city.id,
            osm_id=osm_id,
            name=tags.get("name"),
            highway_type=tags.get("highway"),
            geometry=from_shape(line, srid=4326),
            is_active=True,
        )

        db.add(road)
        db.commit()
        db.refresh(road)

        print("Road inserted successfully!")
        print(f"Database ID: {road.id}")
        print(f"OSM ID: {road.osm_id}")
        print(f"Name: {road.name}")
        print(f"Highway type: {road.highway_type}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    data = fetch_bhavnagar_roads()

    roads = data.get("elements", [])

    print(f"Total roads fetched: {len(roads)}")

    test_insert_one_road(data)