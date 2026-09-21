import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.city import City


def create_bhavnagar():
    db = SessionLocal()

    try:
        existing_city = (
            db.query(City)
            .filter(City.osm_id == "8259844")
            .first()
        )

        if existing_city:
            print(f"Bhavnagar already exists.")
            print(f"ID: {existing_city.id}")
            return

        city = City(
            name="Bhavnagar",
            state="Gujarat",
            country="India",
            osm_id="8259844",
            is_active=True,
        )

        db.add(city)
        db.commit()
        db.refresh(city)

        print("Bhavnagar created successfully!")
        print(f"Database ID: {city.id}")
        print(f"Name: {city.name}")
        print(f"State: {city.state}")
        print(f"OSM ID: {city.osm_id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_bhavnagar()