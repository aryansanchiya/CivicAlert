import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "osm-data" / "bhavnagar-district.geojson"
OUTPUT_FILE = BASE_DIR / "osm-data" / "bhavnagar-boundary.geojson"


def extract_bhavnagar_boundary():
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    boundary_feature = None

    for feature in data["features"]:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})

        if (
            geometry.get("type") == "MultiPolygon"
            and properties.get("admin_level") == "5"
            and properties.get("boundary") == "administrative"
            and properties.get("official_name") == "Bhavnagar District"
        ):
            boundary_feature = feature
            break

    if boundary_feature is None:
        raise RuntimeError(
            "Bhavnagar District boundary was not found."
        )

    geometry = boundary_feature["geometry"]

    print("Bhavnagar District boundary found.")
    print(f"Geometry type: {geometry['type']}")
    print(f"Number of polygons: {len(geometry['coordinates'])}")

    for index, polygon in enumerate(geometry["coordinates"]):
        outer_ring = polygon[0]

        print(
            f"Polygon {index}: "
            f"{len(outer_ring)} boundary points"
        )

        print(f"  First point: {outer_ring[0]}")
        print(f"  Last point:  {outer_ring[-1]}")

    output_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "name": "Bhavnagar",
                    "official_name": "Bhavnagar District",
                    "admin_level": "5",
                    "boundary": "administrative",
                    "ref:LGD:district": "443",
                    "wikidata": "Q854963",
                },
            }
        ],
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output_data, f)

    print()
    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_bhavnagar_boundary()