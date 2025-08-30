from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, func
from app.db.base import Base

class WOD(Base):
    __tablename__ = "wods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text())
    scoring_type: Mapped[str] = mapped_column(String(30))  # "for_time", "amrap", "max_load"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    heats = relationship("Heat", back_populates="wod", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="wod", cascade="all, delete-orphan")