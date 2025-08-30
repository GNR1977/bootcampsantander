from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Integer
from app.db.base import Base

class Heat(Base):
    __tablename__ = "heats"

    id: Mapped[int] = mapped_column(primary_key=True)
    wod_id: Mapped[int] = mapped_column(ForeignKey("wods.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(50))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    capacity: Mapped[int] = mapped_column(Integer)

    wod = relationship("WOD", back_populates="heats")
    # opcional: relação com inscrições/atletas por heat