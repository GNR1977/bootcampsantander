from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Float, DateTime, func, UniqueConstraint
from app.db.base import Base

class Score(Base):
    __tablename__ = "scores"
    __table_args__ = (
        UniqueConstraint("athlete_id", "wod_id", name="uq_score_athlete_wod"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"), index=True)
    wod_id: Mapped[int] = mapped_column(ForeignKey("wods.id", ondelete="CASCADE"), index=True)

    time_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)   # para for_time
    reps: Mapped[int | None] = mapped_column(Integer, nullable=True)           # para amrap
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)      # para max_load
    tie_break_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    points: Mapped[float | None] = mapped_column(Float, nullable=True)  # calculada
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    athlete = relationship("Athlete", back_populates="scores")
    wod = relationship("WOD", back_populates="scores")