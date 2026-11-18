from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app.db import DbSessionDep
from app.exceptions import BusinessException, ErrorCode
from app.models.driver_in_race_model import DriverInRaceModel
from app.models.driver_model import DriverModel
from app.models.race_model import RaceModel
from app.schemas.driver import DriverInRace, DriverRead
from app.schemas.race import RaceRead, RaceCreate, RaceUpdate
from app.services.repository import AbstractAsyncRepository, AsyncRepository

from app.deps import LoggerDep


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
    def __init__(self, db: DbSessionDep, logger: LoggerDep) -> None:
        super().__init__(db, RaceModel, RaceRead, logger)
        self.db = db
        self.logger = logger

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
            self.logger.warning(f"Driver {driver_id} already registered in race {race_id}")
            raise BusinessException.from_code(ErrorCode.DRIVER_ALREADY_REGISTERED)

        driver_in_race = DriverInRaceModel(race_id=race_id, driver_id=driver_id)
        self.db.add(driver_in_race)
        await self.db.flush()
        self.logger.info(f"Driver {driver_id} registered in race {race_id}")
        return DriverInRace.model_validate(driver_in_race)

    async def unregister_driver(self, race_id: int, driver_id: int) -> None:
        registration = await self._get_registration_or_none(race_id, driver_id)
        if registration is None:
            self.logger.warning(f"Driver {driver_id} not registered in race {race_id}")
            raise BusinessException.from_code(ErrorCode.DRIVER_IS_NOT_REGISTERED)

        await self.db.delete(registration)
        await self.db.flush()

        self.logger.info(f"Driver {driver_id} unregistered from race {race_id}")

    async def get_drivers_in_race(self, race_id: int) -> list[DriverRead]:
        if await self.db.get(RaceModel, race_id) is None:
            raise BusinessException.not_found(RaceModel)
        stmt = (
            select(DriverModel)
            .join(DriverModel.race_registrations)
            .where(DriverInRaceModel.race_id == race_id)
        )
        result = await self.db.execute(stmt)
        drivers = result.scalars().unique().all()

        return [DriverRead.model_validate(driver) for driver in drivers]


RaceRepoDep = Annotated[AbstractRaceRepository, Depends(RaceRepository)]
