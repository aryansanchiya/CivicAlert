import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PBF_FILE = BASE_DIR / "osm-data" / "western-zone-latest.osm.pbf"
BOUNDARY_FILE = BASE_DIR / "osm-data" / "bhavnagar-boundary.geojson"
OUTPUT_FILE = BASE_DIR / "osm-data" / "bhavnagar-district.osm.pbf"


def extract_bhavnagar():
    if not PBF_FILE.exists():
        raise FileNotFoundError(
            f"Western Zone PBF not found: {PBF_FILE}"
        )

    if not BOUNDARY_FILE.exists():
        raise FileNotFoundError(
            f"Bhavnagar boundary not found: {BOUNDARY_FILE}"
        )

    print("Extracting Bhavnagar District...")
    print(f"Input:    {PBF_FILE}")
    print(f"Boundary: {BOUNDARY_FILE}")
    print(f"Output:   {OUTPUT_FILE}")
    print()

    subprocess.run(
        [
            "osmium",
            "extract",
            "-p",
            str(BOUNDARY_FILE),
            str(PBF_FILE),
            "-o",
            str(OUTPUT_FILE),
            "--overwrite",
        ],
        check=True,
    )

    if not OUTPUT_FILE.exists():
        raise RuntimeError(
            "Extraction completed but output file was not created."
        )

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)

    print()
    print("Extraction completed.")
    print(f"Output size: {size_mb:.2f} MB")


if __name__ == "__main__":
    extract_bhavnagar()
