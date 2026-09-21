import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PBF_FILE = BASE_DIR / "osm-data" / "bhavnagar-district.osm.pbf"
FILTERED_FILE = BASE_DIR / "osm-data" / "bhavnagar-highways.osm.pbf"


def count_roads():
    if not PBF_FILE.exists():
        raise FileNotFoundError(
            f"PBF file not found: {PBF_FILE}"
        )

    print("Filtering highway ways...")
    print(f"Input: {PBF_FILE}")
    print()

    subprocess.run(
        [
            "osmium",
            "tags-filter",
            str(PBF_FILE),
            "w/highway",
            "-o",
            str(FILTERED_FILE),
            "--overwrite",
        ],
        check=True,
    )

    print("Highway filtering completed.")
    print()

    result = subprocess.run(
        [
            "osmium",
            "fileinfo",
            "-e",
            str(FILTERED_FILE),
        ],
        capture_output=True,
        text=True,
    )

    print(result.stdout)

    size_mb = FILTERED_FILE.stat().st_size / (1024 * 1024)

    print(f"Filtered highway PBF size: {size_mb:.2f} MB")


if __name__ == "__main__":
    count_roads()