import subprocess
import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent

PBF_FILE = BASE_DIR / "osm-data" / "bhavnagar-highways.osm.pbf"
JSON_FILE = BASE_DIR / "osm-data" / "bhavnagar-highways.json"


def export_highways():
    print("Exporting highway ways to JSON...")

    subprocess.run(
        [
            "osmium",
            "export",
            str(PBF_FILE),
            "-o",
            str(JSON_FILE),
            "--overwrite",
        ],
        check=True,
    )

    print("Export completed.")


def analyze():
    with JSON_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    highway_types = Counter()
    named = 0
    unnamed = 0
    total = 0

    for feature in data.get("features", []):
        properties = feature.get("properties", {})

        highway = properties.get("highway")

        if not highway:
            continue

        total += 1
        highway_types[highway] += 1

        if properties.get("name"):
            named += 1
        else:
            unnamed += 1

    print()
    print("Bhavnagar Road Dataset")
    print("=" * 50)
    print(f"Total highway features: {total}")
    print(f"Named:                  {named}")
    print(f"Unnamed:                {unnamed}")

    print()
    print("Highway Type Distribution")
    print("=" * 50)

    for highway_type, count in highway_types.most_common():
        print(f"{highway_type:25} {count}")


def main():
    if not PBF_FILE.exists():
        raise FileNotFoundError(
            f"Highway PBF not found: {PBF_FILE}"
        )

    export_highways()
    analyze()


if __name__ == "__main__":
    main()
