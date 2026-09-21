from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.base import Base
from geoalchemy2 import Geometry

class Road(Base):
    __tablename__ = "roads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)

    osm_id: Mapped[str] = mapped_column(String(50), nullable=True, index=True, unique=True)

    name: Mapped[str] = mapped_column(String(100), nullable=True)

    geometry: Mapped[Geometry] = mapped_column(Geometry(geometry_type="LINESTRING", srid=4326, spatial_index=True), nullable=True)

    highway_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    city = relationship("City", back_populates="roads")

