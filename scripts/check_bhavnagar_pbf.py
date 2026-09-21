import subprocess
import re
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

BOUNDARY_FILE = BASE_DIR / "osm-data" / "bhavnagar-boundary.geojson"
PBF_FILE = BASE_DIR / "osm-data" / "western-zone-latest.osm.pbf"


def get_bhavnagar_extent():
    with BOUNDARY_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    geometry = data["features"][0]["geometry"]

    points = []

    for polygon in geometry["coordinates"]:
        for ring in polygon:
            points.extend(ring)

    longitudes = [point[0] for point in points]
    latitudes = [point[1] for point in points]

    return {
        "min_lon": min(longitudes),
        "max_lon": max(longitudes),
        "min_lat": min(latitudes),
        "max_lat": max(latitudes),
    }


def get_pbf_bbox():
    result = subprocess.run(
        [
            "osmium",
            "fileinfo",
            str(PBF_FILE),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout

    match = re.search(
        r"Bounding boxes:\s*\n\s*\(([^,]+),([^,]+),([^,]+),([^)]+)\)",
        output,
    )

    if not match:
        raise RuntimeError(
            "Could not determine PBF bounding box."
        )

    return {
        "min_lon": float(match.group(1)),
        "min_lat": float(match.group(2)),
        "max_lon": float(match.group(3)),
        "max_lat": float(match.group(4)),
    }


def check_overlap(boundary, pbf):
    longitude_overlap = (
        boundary["min_lon"] <= pbf["max_lon"]
        and boundary["max_lon"] >= pbf["min_lon"]
    )

    latitude_overlap = (
        boundary["min_lat"] <= pbf["max_lat"]
        and boundary["max_lat"] >= pbf["min_lat"]
    )

    return longitude_overlap and latitude_overlap


def main():
    if not BOUNDARY_FILE.exists():
        raise FileNotFoundError(
            f"Boundary file not found: {BOUNDARY_FILE}"
        )

    if not PBF_FILE.exists():
        raise FileNotFoundError(
            f"PBF file not found: {PBF_FILE}"
        )

    boundary = get_bhavnagar_extent()
    pbf = get_pbf_bbox()

    print("Bhavnagar District")
    print("=" * 40)
    print(f"Longitude: {boundary['min_lon']} → {boundary['max_lon']}")
    print(f"Latitude:  {boundary['min_lat']} → {boundary['max_lat']}")

    print()
    print("Western Zone PBF")
    print("=" * 40)
    print(f"Longitude: {pbf['min_lon']} → {pbf['max_lon']}")
    print(f"Latitude:  {pbf['min_lat']} → {pbf['max_lat']}")

    print()
    print("Coverage check")
    print("=" * 40)

    if check_overlap(boundary, pbf):
        print("PASSED: Western Zone overlaps Bhavnagar District.")
    else:
        print("FAILED: Western Zone does NOT overlap Bhavnagar District.")


if __name__ == "__main__":
    main()