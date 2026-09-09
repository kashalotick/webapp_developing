from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.driver_in_race_model import DriverInRaceModel


class DriverModel(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    team: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    race_registrations: Mapped[list["DriverInRaceModel"]] = relationship(
        back_populates="driver", cascade="all, delete-orphan"
    )
