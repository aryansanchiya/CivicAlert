import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OSM_DIR = BASE_DIR / "osm-data"

PBF_URL = (
    "https://download.geofabrik.de/asia/india/"
    "western-zone-latest.osm.pbf"
)

OUTPUT_FILE = OSM_DIR / "western-zone-latest.osm.pbf"


def download_pbf():
    OSM_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        print(f"File already exists: {OUTPUT_FILE}")
        print("Skipping download.")
        return

    print("Downloading Geofabrik Western Zone PBF...")
    print(f"URL: {PBF_URL}")
    print()

    subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--progress-bar",
            PBF_URL,
            "-o",
            str(OUTPUT_FILE),
        ],
        check=True,
    )

    print()
    print("Download completed.")
    print(f"File: {OUTPUT_FILE}")


def verify_pbf():
    if not OUTPUT_FILE.exists():
        raise FileNotFoundError(
            f"PBF file not found: {OUTPUT_FILE}"
        )

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)

    print()
    print("PBF file verification")
    print("=" * 40)
    print(f"Path: {OUTPUT_FILE}")
    print(f"Size: {size_mb:.2f} MB")

    if size_mb < 10:
        raise RuntimeError(
            "Downloaded PBF appears suspiciously small."
        )

    print("Basic file-size check: PASSED")


def main():
    download_pbf()
    verify_pbf()


if __name__ == "__main__":
    main()
