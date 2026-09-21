import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, func

from database.session import SessionLocal
from models.road import Road


def analyze_road_groups():
    db = SessionLocal()

    try:
        print("=" * 70)
        print("BHAVNAGAR ROAD GROUP ANALYSIS")
        print("=" * 70)

        # ---------------------------------------------------------
        # 1. Total roads
        # ---------------------------------------------------------
        total_roads = db.scalar(
            select(func.count(Road.id))
        )

        print(f"\nTotal road segments : {total_roads}")

        # ---------------------------------------------------------
        # 2. Named roads
        # ---------------------------------------------------------
        named_roads = db.scalar(
            select(func.count(Road.id))
            .where(Road.name.is_not(None))
        )

        print(f"Named road segments : {named_roads}")

        # ---------------------------------------------------------
        # 3. Unique road names
        # ---------------------------------------------------------
        unique_names = db.scalar(
            select(func.count(func.distinct(Road.name)))
            .where(Road.name.is_not(None))
        )

        print(f"Unique road names    : {unique_names}")

        # ---------------------------------------------------------
        # 4. Road names with most OSM segments
        # ---------------------------------------------------------
        print("\n" + "-" * 70)
        print("ROAD NAMES WITH MOST OSM SEGMENTS")
        print("-" * 70)

        results = db.execute(
            select(
                Road.name,
                func.count(Road.id).label("segment_count")
            )
            .where(Road.name.is_not(None))
            .group_by(Road.name)
            .order_by(func.count(Road.id).desc())
            .limit(30)
        ).all()

        for index, row in enumerate(results, start=1):
            print(
                f"{index:2}. "
                f"{row.name[:50]:50} "
                f"{row.segment_count:5} segments"
            )

        # ---------------------------------------------------------
        # 5. Road names with multiple highway types
        # ---------------------------------------------------------
        print("\n" + "-" * 70)
        print("ROAD NAMES WITH MULTIPLE HIGHWAY TYPES")
        print("-" * 70)

        results = db.execute(
            select(
                Road.name,
                func.count(func.distinct(Road.highway_type)).label(
                    "highway_type_count"
                ),
                func.count(Road.id).label("segment_count")
            )
            .where(Road.name.is_not(None))
            .group_by(Road.name)
            .having(
                func.count(func.distinct(Road.highway_type)) > 1
            )
            .order_by(func.count(Road.id).desc())
            .limit(30)
        ).all()

        for index, row in enumerate(results, start=1):
            print(
                f"{index:2}. "
                f"{row.name[:50]:50} "
                f"{row.segment_count:5} segments"
            )

        # ---------------------------------------------------------
        # 6. Unnamed segments by highway type
        # ---------------------------------------------------------
        print("\n" + "-" * 70)
        print("UNNAMED ROAD SEGMENTS")
        print("-" * 70)

        results = db.execute(
            select(
                Road.highway_type,
                func.count(Road.id).label("segment_count")
            )
            .where(Road.name.is_(None))
            .group_by(Road.highway_type)
            .order_by(func.count(Road.id).desc())
        ).all()

        for row in results:
            print(
                f"{str(row.highway_type):20} "
                f"{row.segment_count:6} segments"
            )

        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETED")
        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    analyze_road_groups()
