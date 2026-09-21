import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from geoalchemy2.shape import from_shape
from shapely.geometry import LineString
from sqlalchemy import select

from database.session import SessionLocal
from models.city import City
from models.road import Road


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BHAVNAGAR_CITY_ID = 5

JSON_FILE = (
    Path(__file__).resolve().parent.parent
    / "osm-data"
    / "bhavnagar-highways-with-id.json"
)

ALLOWED_HIGHWAY_TYPES = {
    "motorway",
    "motorway_link",
    "trunk",
    "trunk_link",
    "primary",
    "primary_link",
    "secondary",
    "secondary_link",
    "tertiary",
    "tertiary_link",
    "unclassified",
    "residential",
    "living_street",
    "service",
    "busway",
}


def extract_osm_id(feature_id):
    """
    Convert an osmium feature ID such as:

        w22867352

    into:

        22867352
    """

    if not feature_id:
        return None

    if not feature_id.startswith("w"):
        return None

    return feature_id[1:]


def import_roads():

    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"OSM JSON file not found: {JSON_FILE}"
        )

    print("=" * 60)
    print("Bhavnagar Road Import")
    print("=" * 60)

    print(f"Source: {JSON_FILE}")
    print(f"City ID: {BHAVNAGAR_CITY_ID}")

    # --------------------------------------------------
    # Load GeoJSON
    # --------------------------------------------------

    print("\nLoading OSM GeoJSON...")

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    features = data.get("features", [])

    print(f"Total GeoJSON features: {len(features)}")

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    db = SessionLocal()

    try:

        city = db.scalar(
            select(City).where(
                City.id == BHAVNAGAR_CITY_ID
            )
        )

        if not city:
            raise ValueError(
                f"City with ID {BHAVNAGAR_CITY_ID} does not exist."
            )

        print(
            f"Using city: {city.name} "
            f"(ID: {city.id})"
        )

        imported = 0
        updated = 0
        skipped = 0
        invalid_geometry = 0

        # --------------------------------------------------
        # Process features
        # --------------------------------------------------

        for feature in features:

            geometry = feature.get("geometry")

            if not geometry:
                skipped += 1
                continue

            # Only LineString features represent our roads.
            if geometry.get("type") != "LineString":
                skipped += 1
                continue

            properties = feature.get("properties") or {}

            highway_type = properties.get("highway")

            if highway_type not in ALLOWED_HIGHWAY_TYPES:
                skipped += 1
                continue

            # --------------------------------------------------
            # Extract OSM way ID
            # --------------------------------------------------

            osm_id = extract_osm_id(
                feature.get("id")
            )

            if not osm_id:
                skipped += 1
                continue

            coordinates = geometry.get("coordinates", [])

            if len(coordinates) < 2:
                invalid_geometry += 1
                continue

            try:
                line = LineString(coordinates)
            except Exception:
                invalid_geometry += 1
                continue

            # --------------------------------------------------
            # Find existing road
            # --------------------------------------------------

            existing_road = db.scalar(
                select(Road).where(
                    Road.osm_id == osm_id
                )
            )

            if existing_road:

                existing_road.city_id = BHAVNAGAR_CITY_ID
                existing_road.name = properties.get("name")
                existing_road.highway_type = highway_type
                existing_road.geometry = from_shape(
                    line,
                    srid=4326
                )
                existing_road.is_active = True

                updated += 1

            else:

                road = Road(
                    city_id=BHAVNAGAR_CITY_ID,
                    osm_id=osm_id,
                    name=properties.get("name"),
                    highway_type=highway_type,
                    geometry=from_shape(
                        line,
                        srid=4326
                    ),
                    is_active=True,
                )

                db.add(road)

                imported += 1

            # Commit periodically.
            if (imported + updated) % 500 == 0:
                db.commit()

        db.commit()

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("IMPORT COMPLETED")
        print("=" * 60)

        print(f"New roads imported     : {imported}")
        print(f"Existing roads updated : {updated}")
        print(f"Skipped features       : {skipped}")
        print(f"Invalid geometry       : {invalid_geometry}")
        print(f"Total processed        : {imported + updated}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_roads()