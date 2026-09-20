from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.base import Base
from geoalchemy2 import Geometry

class Area(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    geometry: Mapped[Geometry] = mapped_column(Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=True))

    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False, index=True)

    #OpenStreetMap Object ID for the area
    osm_id: Mapped[str] = mapped_column(String(50), nullable=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    city = relationship("City", back_populates="areas")



