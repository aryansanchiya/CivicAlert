import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    city_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cities.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    type: Mapped[str] = mapped_column(String(50), nullable=False, default="municipality")

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    city = relationship("City", back_populates="tenants")