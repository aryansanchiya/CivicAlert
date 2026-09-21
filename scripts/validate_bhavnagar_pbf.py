import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PBF_FILE = BASE_DIR / "osm-data" / "bhavnagar-district.osm.pbf"


def run_osmium(*args):
    result = subprocess.run(
        ["osmium", *args],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


def validate_pbf():
    if not PBF_FILE.exists():
        raise FileNotFoundError(
            f"PBF file not found: {PBF_FILE}"
        )

    size_mb = PBF_FILE.stat().st_size / (1024 * 1024)

    print("Bhavnagar District PBF")
    print("=" * 40)
    print(f"File: {PBF_FILE}")
    print(f"Size: {size_mb:.2f} MB")

    print()
    print("OSM File Information")
    print("=" * 40)

    output = run_osmium(
        "fileinfo",
        str(PBF_FILE),
    )

    print(output)

    if "Bounding boxes:" not in output:
        raise RuntimeError(
            "No bounding box found. The PBF may be empty."
        )

    print("PBF validation: PASSED")


if __name__ == "__main__":
    validate_pbf()
