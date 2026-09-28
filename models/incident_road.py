from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database.base import Base


class IncidentRoad(Base):
    __tablename__ = "incident_roads"

    id = Column(Integer, primary_key=True, index=True)

    incident_id = Column(
        Integer,
        ForeignKey("incidents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    road_id = Column(
        Integer,
        ForeignKey("roads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    incident = relationship(
        "Incident",
        back_populates="affected_roads",
    )

    road = relationship("Road")