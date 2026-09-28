from datetime import datetime
from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)

from sqlalchemy.orm import relationship
from database.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer,
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String(255), nullable=False) 
    description = Column(Text, nullable=True)
    incident_type = Column(String(50), nullable=False, index=True)

    severity = Column(
        String(20),
        nullable=False,
        index=True,
    )

    geometry = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid = 4326,
            spatial_index=True,
        ),
        nullable=False
    )

    starts_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    ends_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    city = relationship("City")

    affected_roads = relationship(
        "IncidentRoad",
        back_populates="incident",
        cascade="all, delete-orphan",
    )

