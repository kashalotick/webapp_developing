from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.race_model import RaceModel
    from app.models.driver_model import DriverModel


class DriverInRaceModel(Base):
    __tablename__ = "drivers_in_races"

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id", ondelete="CASCADE"), primary_key=True
    )
    race_id: Mapped[int] = mapped_column(
        ForeignKey("races.id", ondelete="CASCADE"), primary_key=True
    )

    driver: Mapped["DriverModel"] = relationship(back_populates="race_participations")
    race: Mapped["RaceModel"] = relationship(back_populates="driver_participations")
