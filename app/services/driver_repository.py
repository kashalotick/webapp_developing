from abc import ABC, abstractmethod

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.driver_in_race_model import DriverInRaceModel
from app.models.driver_model import DriverModel
from app.models.race_model import RaceModel
from app.schemas.driver import DriverRead, DriverCreate, DriverUpdate
from app.schemas.race import RaceRead
from app.services.repository import AbstractAsyncRepository, AsyncRepository


class AbstractDriverRepository(AbstractAsyncRepository[DriverModel, DriverCreate, DriverUpdate ,DriverRead], ABC):

    @abstractmethod
    async def change_rating(self, driver_id: int, delta: int) -> DriverRead | None:
        pass

    @abstractmethod
    async def get_driver_races(self, driver_id: int) -> list[RaceRead]:
        pass


class DriverRepository(AbstractDriverRepository, AsyncRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, DriverModel, DriverRead)
        self.db = db

    async def change_rating(self, driver_id: int, delta: int) -> None | DriverRead:
        query = (
            update(DriverModel)
            .where(DriverModel.id == driver_id)
            .values({
                DriverModel.rating: DriverModel.rating + delta
            })
            .returning(DriverModel)
        )
        result = await self.db.scalar(query)
        await self.db.flush()

        if not result:
            return None
        return DriverRead.model_validate(result)


    async def get_driver_races(self, driver_id: int) -> list[RaceRead]:
        stmt = (
            select(RaceModel)
            .join(RaceModel.driver_registrations)
            .where(DriverInRaceModel.driver_id == driver_id)
        )
        result = await self.db.execute(stmt)
        races = result.scalars().unique().all()

        return [RaceRead.model_validate(race) for race in races]





