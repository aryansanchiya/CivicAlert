import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import func
from database.session import SessionLocal
from models.road import Road


def check_duplicates():
    db = SessionLocal()

    try:
        duplicates = (
            db.query(
                Road.osm_id,
                func.count(Road.id).label("count"),
            )
            .filter(Road.osm_id.isnot(None))
            .group_by(Road.osm_id)
            .having(func.count(Road.id) > 1)
            .all()
        )

        if not duplicates:
            print("No duplicate OSM IDs found.")
            return

        print("Duplicate OSM IDs found:")
        for osm_id, count in duplicates:
            print(f"OSM ID: {osm_id} | Count: {count}")

    finally:
        db.close()


if __name__ == "__main__":
    check_duplicates()
