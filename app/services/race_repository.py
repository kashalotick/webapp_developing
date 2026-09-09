from abc import ABC, abstractmethod

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BusinessException, ErrorCode
from app.models.driver_in_race_model import DriverInRaceModel
from app.models.driver_model import DriverModel
from app.models.race_model import RaceModel
from app.schemas.driver import DriverInRace, DriverRead
from app.schemas.race import RaceRead, RaceCreate, RaceUpdate
from app.services.repository import AbstractAsyncRepository, AsyncRepository


class AbstractRaceRepository(AbstractAsyncRepository[RaceModel, RaceCreate, RaceUpdate, RaceRead], ABC):
    @abstractmethod
    async def register_driver(self, race_id: int, driver_id: int) -> DriverInRace:
        pass

    @abstractmethod
    async def unregister_driver(self, race_id: int, driver_id: int) -> None:
        pass


    @abstractmethod
    async def get_drivers_in_race(self, race_id: int) -> list[DriverRead]:
        pass


class RaceRepository(AbstractRaceRepository, AsyncRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, RaceModel, RaceRead)
        self.db = db

    async def delete(self, entity_id: int) -> bool:
        await super().delete(entity_id)
        query = delete(DriverInRaceModel).where(DriverInRaceModel.race_id == entity_id).returning(DriverInRaceModel.race_id)
        result = await self.db.execute(query)
        await self.db.flush()
        return len(result.all()) > 0


    async def _get_registration_or_none(self, race_id: int, driver_id: int) -> DriverInRaceModel | None:
        race = await self.db.get(RaceModel, race_id)
        driver = await self.db.get(DriverModel, driver_id)
        if race is None:
            raise BusinessException.not_found(RaceModel)
        if driver is None:
            raise BusinessException.not_found(DriverModel)

        query = select(DriverInRaceModel).where(
            DriverInRaceModel.race_id == race_id,
            DriverInRaceModel.driver_id == driver_id
        )
        result = await self.db.scalar(query)
        return result

    async def register_driver(self, race_id: int, driver_id: int) -> DriverInRace:
        registration = await self._get_registration_or_none(race_id, driver_id)
        if registration is not None:
            raise BusinessException.from_code(ErrorCode.DRIVER_ALREADY_REGISTERED)

        driver_in_race = DriverInRace(race_id=race_id, driver_id=driver_id)
        self.db.add(driver_in_race)
        await self.db.flush()
        return driver_in_race

    async def unregister_driver(self, race_id: int, driver_id: int) -> None:
        registration = await self._get_registration_or_none(race_id, driver_id)
        if registration is None:
            raise BusinessException.from_code(ErrorCode.DRIVER_IS_NOT_REGISTERED)

        driver_in_race = DriverInRace(race_id=race_id, driver_id=driver_id)
        await self.db.delete(driver_in_race)


    async def get_drivers_in_race(self, race_id: int) -> list[DriverRead]:
        stmt = (
            select(DriverModel)
            .join(DriverModel.race_registrations)
            .where(DriverInRaceModel.race_id == race_id)
        )
        result = await self.db.execute(stmt)
        drivers = result.scalars().unique().all()

        return [DriverRead.model_validate(driver) for driver in drivers]



