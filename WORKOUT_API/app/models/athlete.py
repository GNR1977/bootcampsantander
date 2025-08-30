from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from app.db.base import Base

class Athlete(Base):
    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    division: Mapped[str] = mapped_column(String(50))  # Rx, Scaled
    gender: Mapped[str] = mapped_column(String(10))    # Male, Female
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    scores = relationship("Score", back_populates="athlete", cascade="all, delete-orphan")