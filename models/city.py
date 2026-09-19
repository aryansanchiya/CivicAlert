# app/models/city.py

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from database.base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False, default="India")

    # OpenStreetMap administrative boundary ID
    osm_id = Column(String(50), nullable=True, unique=True)

    # City boundary from OpenStreetMap
    # boundary = Column(
    #     Geometry(
    #         geometry_type="MULTIPOLYGON",
    #         srid=4326,
    #         spatial_index=True
    #     ),
    #     nullable=True
    # )

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    tenants = relationship("Tenant", back_populates="city")
    