from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, Interval, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.driver_in_race_model import DriverInRaceModel


class RaceModel(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration: Mapped[timedelta] = mapped_column(Interval, nullable=False)
    track: Mapped[str] = mapped_column(String(255), nullable=False)

    driver_registrations: Mapped[list["DriverInRaceModel"]] = relationship(
        back_populates="race", cascade="all, delete-orphan"
    )
